import time
import threading

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class Kitchen:
    def __init__(self, controller):
        # Pin settings
        self.CONTACTOR_PIN_1 = 21
        self.CONTACTOR_PIN_2 = 22
        self.LED_PIN = 23

        # Pin initialization
        GPIO.setup(self.CONTACTOR_PIN_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.CONTACTOR_PIN_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.LED_PIN, GPIO.OUT)

        GPIO.output(self.LED_PIN, GPIO.LOW)

        # controller is the mother class variable
        self.controller = controller

        # initialization and run of subprograms in parallelization
        run = threading.Thread(target=self._run)
        run.start()

    # Subprogram witch looks the window contactors to alight the LED
    def _run(self):
        lock = threading.Lock()
        lock.acquire()
        status_conta_1 = GPIO.input(self.CONTACTOR_PIN_1)
        status_conta_2 = GPIO.input(self.CONTACTOR_PIN_2)
        status_led = status_conta_1 or status_conta_2
        while self.controller.valid:
            if (GPIO.input(self.CONTACTOR_PIN_1) or GPIO.input(self.CONTACTOR_PIN_2)) != status_led:
                status_led = not status_led
                self.controller.changement_variable('Kitchen', 'LED', status_led)
                GPIO.output(self.LED_PIN, status_led)

            if status_conta_1 != GPIO.input(self.CONTACTOR_PIN_1):
                status_conta_1 = not status_conta_1
                self.controller.changement_variable('Kitchen', 'CONTACT_1', status_conta_1)
            if status_conta_2 != GPIO.input(self.CONTACTOR_PIN_2):
                status_conta_2 = not status_conta_2
                self.controller.changement_variable('Kitchen', 'CONTACT_2', status_conta_2)

            time.sleep(0.01)
        lock.release()


    def _stop(self):
        GPIO.output(self.LED_PIN, GPIO.LOW)
        
