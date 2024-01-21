import time
import threading

import RPi.GPIO as GPIO
import Adafruit_DHT

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class Sauna:
    def __init__(self, controller):
        # Pin settings
        self.DHT_PIN = 3
        self.LED_PIN = 28
        # self.EN_Sauna_PIN = 2
        self.CONTACTOR_PIN = 1

        # Pin initialization
        GPIO.setup(self.LED_PIN, GPIO.OUT)
        GPIO.setup(self.CONTACTOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.output(self.LED_PIN, GPIO.LOW)
        
        self.controller = controller
        
        run = threading.Thread(target=self._run)
        run.start()

    def _run(self):
        lock = threading.Lock()
        lock.acquire()
        status_led = GPIO.input(self.CONTACTOR_PIN)
        status_conta = GPIO.input(self.CONTACTOR_PIN)
        while self.controller.valid:
            change_led = False
            if GPIO.input(self.CONTACTOR_PIN) and not status_led:
                status_led = True
                change_led = True
            elif not GPIO.input(self.CONTACTOR_PIN) and status_led:
                status_led = False
                change_led = False
            if change_led:
                self.controller.changement_variable('Sauna', 'LED', status_led)
                GPIO.output(self.LED_PIN, status_led)

            if status_conta != GPIO.input(self.CONTACTOR_PIN):
                status_conta = not status_conta
                self.controller.changement_variable('Sauna', 'CONTACT', status_conta)
            humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, self.DHT_PIN)
            if self.controller.valid:
                self.controller.changement_variable('Sauna', 'HUMIDITY', humidity)
                self.controller.changement_variable('Sauna', 'TEMPERATURE', temperature)
            time.sleep(0.01)
            
        lock.release()

    def _stop(self):
        GPIO.output(self.LED_PIN, GPIO.LOW)
