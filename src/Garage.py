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

        self.controller = controller

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

        sensors = threading.Thread(target=self._sensors)
        mesuring_distance = threading.Thread(target=self._mesuring_distance)
        run_portal = threading.Thread(target=self._run_portal)
        run_portal.start()
        sensors.start()
        mesuring_distance.start()

    def _mesuring_distance(self):
        lock = threading.Lock()
        lock.acquire()
        val_distance = None
        start_time = time.time()
        stop_time = time.time()
        while self.controller.valid:
            GPIO.output(self.TRIG, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(self.TRIG, GPIO.LOW)
            
            first_time = time.time()

            while not GPIO.input(self.ECHO) and self.controller.valid:
                start_time = time.time()
                if start_time-first_time >= 0.001:
                    break

            while GPIO.input(self.ECHO) and self.controller.valid:
                stop_time = time.time()
            
            ptime = start_time-first_time
            distance = ptime * 34300 / 2
            temp_val_distance = val_distance
            if distance < 5 and self.controller.valid:
                val_distance = 0
                if temp_val_distance != val_distance:
                    GPIO.output(self.GREEN_LED, False)
                    GPIO.output(self.YELLOW_LED, False)
                    GPIO.output(self.RED_LED, True)
                    self.controller.changement_variable('Garage', 'LEDS', 'Red')
            elif distance < 10 and self.controller.valid:
                val_distance = 1
                if temp_val_distance != val_distance:
                    GPIO.output(self.GREEN_LED, False)
                    GPIO.output(self.YELLOW_LED, True)
                    GPIO.output(self.RED_LED, False)
                    self.controller.changement_variable('Garage', 'LEDS', 'Yellow')
            elif distance < 20 and self.controller.valid:
                val_distance = 2
                if temp_val_distance != val_distance:
                    GPIO.output(self.GREEN_LED, True)
                    GPIO.output(self.YELLOW_LED, False)
                    GPIO.output(self.RED_LED, False)
                    self.controller.changement_variable('Garage', 'LEDS', 'Green')
            elif self.controller.valid:
                val_distance = 3
                if temp_val_distance != val_distance:
                    GPIO.output(self.GREEN_LED, False)
                    GPIO.output(self.YELLOW_LED, False)
                    GPIO.output(self.RED_LED, False)
                    self.controller.changement_variable('Garage', 'LEDS', 'Off')
                    
            time.sleep(0.2)
        lock.release()

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
            
            if self.have_changed:
                if self.is_limit_1 and not self.is_motor_clockwise and self.is_motor_running:
                    GPIO.output(self.pin_high, GPIO.LOW)
                    self.is_motor_clockwise = not self.is_motor_clockwise
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

    def _run_portal(self):
        lock = threading.Lock()
        lock.acquire()
        time.sleep(0.5)

        while self.controller.valid:
            while self.is_button_pressed:
                if not self.controller.valid:
                    self.is_button_pressed = False
            
            if not self.is_motor_running and (not self.is_barriere_brocken or (self.is_barriere_brocken and not self.is_motor_clockwise)) and self.controller.valid:
                if self.is_limit_2 and self.is_motor_clockwise: # A voir pour ca
                    self.is_motor_clockwise = False
                    self.controller.changement_variable('Garage', 'Clockwise', self.is_motor_clockwise)
                elif self.is_limit_1 and not self.is_motor_clockwise:
                    self.is_motor_clockwise = True
                    self.controller.changement_variable('Garage', 'Clockwise', self.is_motor_clockwise)

                if self.is_motor_clockwise:
                    self.pin_low = self.in2_pin
                    self.pin_high = self.in1_pin
                    self.switch_clock = self.limit_switch_pin2
                else:
                    self.pin_low = self.in1_pin
                    self.pin_high = self.in2_pin
                    self.switch_clock = self.limit_switch_pin1

                GPIO.output(self.pin_low, GPIO.LOW)
                GPIO.output(self.pin_high, GPIO.HIGH)
                self.is_motor_running = True
                self.controller.changement_variable('Garage', 'Motor', self.is_motor_running)
            elif self.is_motor_running:
                GPIO.output(self.pin_high, GPIO.LOW)
                self.is_motor_running = False
                self.is_motor_clockwise = not self.is_motor_clockwise
                self.controller.changement_variable('Garage', 'Motor', self.is_motor_running)
                self.controller.changement_variable('Garage', 'Clockwise', self.is_motor_clockwise)
            elif self.is_barriere_brocken:
                self.is_motor_clockwise = False
                self.controller.changement_variable('Garage', 'Clockwise', self.is_motor_clockwise)

            
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
