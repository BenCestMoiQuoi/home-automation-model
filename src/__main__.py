import threading
import tkinter as tk
import sys
import time

# import classes
from House.Bathroom import Bathroom
from House.Bedroom import Bedroom
from House.Garage import Garage
from House.Kitchen import Kitchen
from House.Salon import Salon
from House.Sauna import Sauna
import House.Page as P


import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


NAME_PROJECT = 'House'
NAME_PAGES = ('House', 'Bathroom', 'Bedroom', 'Garage', 'Kitchen', 'Salon', 'Sauna')
PAGES = {
    'House': P.House, 
    'Bathroom': P.Bathroom, 
    'Bedroom': P.Bedroom,
    'Garage': P.Garage,
    'Kitchen': P.Kitchen,
    'Salon': P.Salon,
    'Sauna': P.Sauna
}
SIZE_PAGES = {
    'House': ('390x149'), 
    'Bathroom': ('300x186'), 
    'Bedroom': ('300x186'), 
    'Garage': ('326x337'), 
    'Kitchen': ('318x186'), 
    'Salon': ('300x154'), 
    'Sauna': ('320x300')
}


class House:
    def __init__(self, controller):
    # It's possible to 
        self.pieces = [Bathroom(controller),
                       Bedroom(controller),
                       Garage(controller),
                       Kitchen(controller),
                       Salon(controller),
                       Sauna(controller)
                       ]

    def _stop(self):
        for i in self.pieces:
            i._stop()


# Main class, witch initialize all the sub routine and the interfaces
# When a button is pressed, the interface changed and is resized
# All interfaces are charged at the beginning of the program on the self.frame variable
class Main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, NAME_PROJECT)


        self.page = 0

        self.bind('<KeyPress-Escape>', self.keypress_enter)

        # creation of the main container (for all the interfaces)
        container = tk.Frame(self)
        container.pack(side="top")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # lunch of each interface
        self.frames = {}
        for n in NAME_PAGES:
            frame = PAGES[n](container, self)
            frame.grid(row=0, column=0, sticky='nsew')
            
            self.frames[n] = frame
        self.page = 'House'
        self.change_page()

        self.valid = True
        # initialisation of all the sub routine (call of House class)
        self.house = House(self)

        self.mainloop()

    # At the end of the interface, when the button "Leave" is pressed, the GPIO pins are realessed
    def on_closing(self):
        self.valid = False
        time.sleep(1)
        self.house._stop() # Put on GPIO.LOW all the output pins
        time.sleep(1)
        GPIO.cleanup() # Here
        self.destroy()

    # Short cut Escape
    def keypress_enter(self, key):
        if self.page == 'House' and key.keysym == 'Escape':
            self.on_closing()
        elif self.page != 'House' and key.keysym == 'Escape':
            self.page = 'House'
            self.change_page()
        
    # Changement page function
    def change_page(self, page=''):
        # put the wrong interface on the first plan
        if page in self.frames.keys():
            self.page = page
        frame = self.frames[self.page] # variable to put on first plan
        self.geometry(SIZE_PAGES[self.page]) # resized
        frame.tkraise() # First plan effective

    # When an variable changed on the "room" programs, this function is called
    # and permit to change in real time each variables of the interfaces
    def changement_variable(self, Page, Variable, status):
        self.frames[Page].changement_variable(Variable, status)

# Beginning of the main program
        
# Lock the paralelization
lock = threading.Lock()
lock.acquire()

Main()

# Release the paralelization
lock.release()
# the release may take a little time (maximum 30s)


# End of the main program