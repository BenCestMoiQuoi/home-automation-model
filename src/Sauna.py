import time
import threading

import RPi.GPIO as GPIO
import Adafruit_DHT

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# This room is not totaly cabled, if you want you have just to cabled 
# and note the wrong pins. The programs work, without the Peltier and the LED linked
class Sauna:
    def __init__(self, controller):
        # Pin settings
        self.DHT_PIN = 30
        self.LED1_PIN = 28
        # self.EN_Sauna_PIN = 2 # Peltier Pin, it's not used in this program, but we know that it's possible
        # self.LED2_PIN =  # It's the Led linked with the Peltier, to know how it heat
        self.CONTACTOR_PIN = 29

        # Pin initialization
        GPIO.setup(self.LED_PIN, GPIO.OUT)
        GPIO.setup(self.CONTACTOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.output(self.LED_PIN, GPIO.LOW)

        # controller is the mother class variable
        self.controller = controller
        
        # initialization and run of subprograms in parallelization
        run = threading.Thread(target=self._run)
        run.start()

    # Subprogram witch looks the door contactor to alight the LED and communicate with the DHT sensor
    # to know the temperature and the humidity. It's possible to lunch the Peltier with temperature and humidity parameters.
    def _run(self):
        lock = threading.Lock()
        lock.acquire()
        status_led1 = GPIO.input(self.CONTACTOR_PIN)
        status_conta = GPIO.input(self.CONTACTOR_PIN)
        while self.controller.valid:
            if GPIO.input(self.CONTACTOR_PIN) and not status_led1:
                status_led1 = not status_led1
                self.controller.changement_variable('Sauna', 'LED', status_led1)
                GPIO.output(self.LED1_PIN, status_led1)

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
        GPIO.output(self.LED1_PIN, GPIO.LOW)
