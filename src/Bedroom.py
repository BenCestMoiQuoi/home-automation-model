import time
import threading

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

TIMMER_LIGHT = 5
class Bedroom:
    def __init__(self, controller):
        # Pin settings
        self.PIR_PIN = 27
        self.CONTACTOR_PIN = 25
        self.LED_PIN = 26

        # Pin initialization
        GPIO.setup(self.CONTACTOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.PIR_PIN, GPIO.IN)
        GPIO.setup(self.LED_PIN, GPIO.OUT)

        GPIO.output(self.LED_PIN, GPIO.LOW)

        self.controller = controller

        # Creating the loop
        run = threading.Thread(target=self._run)
        run.start()


    def _run(self):
        lock = threading.Lock()
        lock.acquire()
        status_led = GPIO.input(self.CONTACTOR_PIN)
        status_conta = GPIO.input(self.CONTACTOR_PIN)
        status_pir = not GPIO.input(self.PIR_PIN)
        while self.controller.valid:            
            change_led = False
            if GPIO.input(self.CONTACTOR_PIN) and not status_led:
                status_led = True
                change_led = True
            elif not GPIO.input(self.CONTACTOR_PIN) and status_led:
                status_led = False
                change_led = True
            if change_led:
                self.controller.changement_variable('Bedroom', 'LED', status_led)
                GPIO.output(self.LED_PIN, status_led)

            if status_pir != GPIO.input(self.PIR_PIN):
                status_pir = not status_pir
                self.controller.changement_variable('Bedroom', 'PIR', status_pir)
            if status_conta != GPIO.input(self.CONTACTOR_PIN):
                status_conta = not status_conta
                self.controller.changement_variable('Bedroom', 'CONTACT', status_conta)

            time.sleep(0.01)
        lock.release()

    def _stop(self):
        self.relay = 0
        self.relay_valid = False
        GPIO.output(self.LED_PIN, False)
