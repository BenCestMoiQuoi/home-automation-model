import time
import threading

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
class Garage:
    def __init__(self, controller):
        # Pin settings
        self.TRIG = 14
        self.ECHO = 13
        self.GREEN_LED = 16
        self.YELLOW_LED = 17
        self.RED_LED = 18

        self.in1_pin = 12
        self.in2_pin = 8

        self.button_pin = 4
        self.limit_switch_pin1 = 2
        self.limit_switch_pin2 = 3
        self.optical_barrier_pin = 19

        # Pin initialization
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)
        GPIO.setup(self.GREEN_LED, GPIO.OUT)
        GPIO.setup(self.YELLOW_LED, GPIO.OUT)
        GPIO.setup(self.RED_LED, GPIO.OUT)

        GPIO.setup(self.in1_pin, GPIO.OUT)
        GPIO.setup(self.in2_pin, GPIO.OUT)

        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.limit_switch_pin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.limit_switch_pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.optical_barrier_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.output(self.TRIG, GPIO.LOW)
        GPIO.output(self.GREEN_LED, GPIO.LOW)
        GPIO.output(self.YELLOW_LED, GPIO.LOW)
        GPIO.output(self.RED_LED, GPIO.LOW)
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.LOW)

        # controller is the mother class variable
        self.controller = controller

        # initialization of all variables for programs
        self.is_motor_running = False
        self.is_motor_clockwise = True
        self.is_button_pressed = False
        self.is_barriere_brocken = False
        self.is_barriere_limit = False
        self.is_limit_1 = False
        self.is_limit_2 = False

        self.have_changed = False
        
        self.pin_low = self.in1_pin
        self.pin_high = self.in2_pin

        # initialization and run of subprograms in parallelization
        sensors = threading.Thread(target=self._sensors)
        mesuring_distance = threading.Thread(target=self._mesuring_distance)
        run_portal = threading.Thread(target=self._run_portal)
        run_portal.start()
        sensors.start()
        mesuring_distance.start()

    # Subprogram witch mesuring the distance between the wall and the car with ultrason sensor
    # and show the distance with 3 LEDs (green, orange and red) 
    def _mesuring_distance(self):
        lock = threading.Lock()
        lock.acquire()
        val_distance = None
        while self.controller.valid:
            GPIO.output(self.TRIG, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(self.TRIG, GPIO.LOW)
            
            first_time = time.time()

            # mesuring the time between send and receive of the wave
            while not GPIO.input(self.ECHO) and self.controller.valid:
                start_time = time.time()
                if start_time-first_time >= 0.001:
                    break
            
            ptime = start_time-first_time
            distance = ptime * 34300 / 2
            temp_val_distance = val_distance
            # Edit if it have a changment the color of the LEDs
            if distance < 5:
                val_distance = 0
                if temp_val_distance != val_distance:
                    GPIO.output(self.GREEN_LED, False)
                    GPIO.output(self.YELLOW_LED, False)
                    GPIO.output(self.RED_LED, True)
                    self.controller.changement_variable('Garage', 'LEDS', 'Red')
            elif distance < 10:
                val_distance = 1
                if temp_val_distance != val_distance:
                    GPIO.output(self.GREEN_LED, False)
                    GPIO.output(self.YELLOW_LED, True)
                    GPIO.output(self.RED_LED, False)
                    self.controller.changement_variable('Garage', 'LEDS', 'Yellow')
            elif distance < 20:
                val_distance = 2
                if temp_val_distance != val_distance:
                    GPIO.output(self.GREEN_LED, True)
                    GPIO.output(self.YELLOW_LED, False)
                    GPIO.output(self.RED_LED, False)
                    self.controller.changement_variable('Garage', 'LEDS', 'Green')
            else:
                val_distance = 3
                if temp_val_distance != val_distance:
                    GPIO.output(self.GREEN_LED, False)
                    GPIO.output(self.YELLOW_LED, False)
                    GPIO.output(self.RED_LED, False)
                    self.controller.changement_variable('Garage', 'LEDS', 'Off')
                    
            time.sleep(0.2)
        lock.release()

    # Subprogram witch sound all sensors to change variables and edit the house interface
    # Limite up, limite down, optical barriere and button.
    def _sensors(self):
        lock = threading.Lock()
        lock.acquire()
        self.is_limit_1 = GPIO.input(self.limit_switch_pin1)
        self.is_limit_2 = GPIO.input(self.limit_switch_pin2)
        self.is_barriere_brocken = GPIO.input(self.optical_barrier_pin)
        self.is_button_pressed = GPIO.input(self.button_pin)
        while self.controller.valid:
            self.have_changed = False
            if GPIO.input(self.limit_switch_pin1) == self.is_limit_1:
                self.is_limit_1 = not self.is_limit_1
                self.have_changed = True
                self.controller.changement_variable('Garage', 'Limit_1', self.is_limit_1)

            if GPIO.input(self.limit_switch_pin2) == self.is_limit_2:
                self.is_limit_2 = not self.is_limit_2
                self.have_changed = True
                self.controller.changement_variable('Garage', 'Limit_2', self.is_limit_2)

            if GPIO.input(self.optical_barrier_pin) == self.is_barriere_brocken:
                self.is_barriere_brocken = not self.is_barriere_brocken
                self.have_changed = True
                self.controller.changement_variable('Garage', 'Barriere', self.is_barriere_brocken)

            if GPIO.input(self.button_pin) != self.is_button_pressed:
                self.is_button_pressed = not self.is_button_pressed
                self.have_changed = True
                self.controller.changement_variable('Garage', 'Button', self.is_button_pressed)
            # look if have a change on sensor to update the state of the motor If it's necessary
            if self.have_changed:
                if self.is_limit_1 and not self.is_motor_clockwise and self.is_motor_running:
                    GPIO.output(self.pin_high, GPIO.LOW) # stop the motor
                    self.is_motor_clockwise = not self.is_motor_clockwise # change the next rotation of the motor
                    self.is_motor_running = False
                    self.controller.changement_variable('Garage', 'Clockwise', self.is_motor_clockwise)
                    self.controller.changement_variable('Garage', 'Motor', self.is_motor_running)
                if self.is_limit_2 and self.is_motor_clockwise and self.is_motor_running:
                    GPIO.output(self.pin_high, GPIO.LOW)
                    self.is_motor_clockwise = not self.is_motor_clockwise
                    self.is_motor_running = False
                    self.controller.changement_variable('Garage', 'Clockwise', self.is_motor_clockwise)
                    self.controller.changement_variable('Garage', 'Motor', self.is_motor_running)
                if self.is_barriere_brocken and not self.is_motor_clockwise and self.is_motor_running:
                    GPIO.output(self.pin_high, GPIO.LOW)
                    self.is_motor_clockwise = not self.is_motor_clockwise
                    self.is_motor_running = False
                    self.controller.changement_variable('Garage', 'Clockwise', self.is_motor_clockwise)
                    self.controller.changement_variable('Garage', 'Motor', self.is_motor_running)
        lock.release()

    # Subprogram witch run the portal with parameters already define
    def _run_portal(self):
        lock = threading.Lock()
        lock.acquire()
        time.sleep(0.5)

        while self.controller.valid:
        # If the button is pressed
            while self.is_button_pressed:
                if not self.controller.valid:
                    self.is_button_pressed = False
            # If motor sleep and optical barriere free or optical barriere break and portal sens up
            if not self.is_motor_running and (not self.is_barriere_brocken or (self.is_barriere_brocken and not self.is_motor_clockwise)) and self.controller.valid:
                # change the clockwise if it's necessary
                if self.is_limit_2 and self.is_motor_clockwise:
                    self.is_motor_clockwise = False
                    self.controller.changement_variable('Garage', 'Clockwise', self.is_motor_clockwise)
                elif self.is_limit_1 and not self.is_motor_clockwise:
                    self.is_motor_clockwise = True
                    self.controller.changement_variable('Garage', 'Clockwise', self.is_motor_clockwise)
                # change the High and Low pin for the motor (rotation sens)
                if self.is_motor_clockwise:
                    self.pin_low = self.in2_pin
                    self.pin_high = self.in1_pin
                    self.switch_clock = self.limit_switch_pin2
                else:
                    self.pin_low = self.in1_pin
                    self.pin_high = self.in2_pin
                    self.switch_clock = self.limit_switch_pin1
                # define motor running
                GPIO.output(self.pin_low, GPIO.LOW)
                GPIO.output(self.pin_high, GPIO.HIGH)
                self.is_motor_running = True
                self.controller.changement_variable('Garage', 'Motor', self.is_motor_running)
            # If motor running, stop it
            elif self.is_motor_running:
                GPIO.output(self.pin_high, GPIO.LOW)
                self.is_motor_running = False
                self.is_motor_clockwise = not self.is_motor_clockwise
                self.controller.changement_variable('Garage', 'Motor', self.is_motor_running)
                self.controller.changement_variable('Garage', 'Clockwise', self.is_motor_clockwise)
            # If motor sleep, barriere break and portal clockwise to down
            elif self.is_barriere_brocken:
                # change the clockwise, you can after push an other time the button to make motor running
                self.is_motor_clockwise = False
                self.controller.changement_variable('Garage', 'Clockwise', self.is_motor_clockwise)
            # check if the button is realsed
            while not self.is_button_pressed:
                if not self.controller.valid:
                    self.is_button_pressed = True 
        lock.release()

    def _stop(self):
        GPIO.output(self.TRIG, GPIO.LOW)
        GPIO.output(self.GREEN_LED, GPIO.LOW)
        GPIO.output(self.YELLOW_LED, GPIO.LOW)
        GPIO.output(self.RED_LED, GPIO.LOW)

        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.LOW)
