import time
import threading

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
class Salon:
    def __init__(self, controller):
        # Pin settings
        self.CONTACTOR_PIN = 24
        self.LED_PIN = 5

        # Pin initialization
        GPIO.setup(self.CONTACTOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.LED_PIN, GPIO.OUT)

        GPIO.output(self.LED_PIN, GPIO.LOW)

        # controller is the mother class variable
        self.controller = controller

        # initialization and run of subprograms in parallelization
        run = threading.Thread(target=self._run)
        run.start()

    # Subprogram witch looks the window contactor to alight the LED
    def _run(self):
        lock = threading.Lock()
        lock.acquire()
        status_led = GPIO.input(self.CONTACTOR_PIN)
        status_conta = GPIO.input(self.CONTACTOR_PIN)
        while self.controller.valid:
            if GPIO.input(self.CONTACTOR_PIN) != status_led:
                status_led = not status_led
                self.controller.changement_variable('Salon', 'LED', status_led)
                GPIO.output(self.LED_PIN, status_led)

            if status_conta != GPIO.input(self.CONTACTOR_PIN):
                status_conta = not status_conta
                self.controller.changement_variable('Salon', 'CONTACT', status_conta)

            time.sleep(0.01)
        lock.release()

    def _stop(self):
        GPIO.output(self.LED_PIN, False)
