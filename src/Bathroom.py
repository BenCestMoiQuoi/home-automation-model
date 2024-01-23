import time
import threading

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# On this program, if you want to add a light pannel, it's possible, 
# you have to decomment each lines where "self.RELAY_PIN" is
class Bathroom:
    def __init__(self, controller):
        # Pin settings
        self.PIR_PIN = 9
        self.CONTACTOR_PIN = 11
        self.LED_PIN = 10
        # self.RELAY_PIN =    # the pin for the LED pannel

        # Pin initialization
        GPIO.setup(self.CONTACTOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.PIR_PIN, GPIO.IN)
        GPIO.setup(self.LED_PIN, GPIO.OUT)
        # GPIO.setup(self.RELAY_PIN, GPIO.OUT)

        GPIO.output(self.LED_PIN, GPIO.LOW)
        # GPIO.output(self.RELAY_PIN, GPIO.LOW)

        # controller is the mother class variable
        self.controller = controller

        # initialization and run of subprograms in parallelization
        run = threading.Thread(target=self._run)
        run.start()

    # Subprogram witch looks the window contactor to alight the LED and check the PIR sensor
    # to alight the LED panel
    def _run(self):
        lock = threading.Lock()
        lock.acquire()
        status_pir = not GPIO.input(self.PIR_PIN)
        status_led = GPIO.input(self.CONTACTOR_PIN)
        status_conta = GPIO.input(self.CONTACTOR_PIN)
        while self.controller.valid:            
            change_led = False
            if GPIO.input(self.CONTACTOR_PIN) and not status_led:
                status_led = True
                change_led = True
            elif not GPIO.input(self.CONTACTOR_PIN) and status_led:
                status_led = False
                change_led = True
            if change_led:
                self.controller.changement_variable('Bathroom', 'LED', status_led)
                GPIO.output(self.LED_PIN, status_led)

            if status_pir != GPIO.input(self.PIR_PIN):
                status_pir = not status_pir
                # GPIO.output(self.RELAY_PIN, status_pir)
                self.controller.changement_variable('Bathroom', 'PIR', status_pir)
            if status_conta != GPIO.input(self.CONTACTOR_PIN):
                status_conta = not status_conta
                self.controller.changement_variable('Bathroom', 'CONTACT', status_conta)

            time.sleep(0.01)
        lock.release()

    def _stop(self):
        GPIO.output(self.LED_PIN, GPIO.LOW)
        # GPIO.output(self.RELAY_PIN, GPIO.LOW)
