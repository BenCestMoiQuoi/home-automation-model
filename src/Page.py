import tkinter as tk

# All the parameters are changed in real time with the changement_variable function


# Main interface, it's possible to choose a room interface
# thanks to button
class House(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # initialization of each button
        self.l_text = Label(self, text="Pannel control of the House")
        self.f_house = tk.Frame(self) # a frame is the simplest way to make other buttons
        self.b_quit = Button(self, text="Leave", command=controller.on_closing)

        self.b_bathroom = Button(self.f_house, text='Bathroom', command=lambda p='Bathroom': controller.change_page(p))
        self.b_bedroom = Button(self.f_house, text='Bedroom', command=lambda p='Bedroom': controller.change_page(p))
        self.b_garage = Button(self.f_house, text='Garage', command=lambda p='Garage': controller.change_page(p))
        self.b_kitchen = Button(self.f_house, text='Kitchen', command=lambda p='Kitchen': controller.change_page(p))
        self.b_salon = Button(self.f_house, text='Salon', command=lambda p='Salon': controller.change_page(p))
        self.b_sauna = Button(self.f_house, text='Sauna', command=lambda p='Sauna': controller.change_page(p))

        # gird of each button
        self.l_text.grid(row=0, column=0, columnspan=2)
        self.f_house.grid(row=1, column=0)
        self.b_quit.grid(row=2, column=1)

        self.b_bathroom.grid(row=0, column=0)
        self.b_bedroom.grid(row=0, column=1)
        self.b_garage.grid(row=0, column=2)
        self.b_kitchen.grid(row=1, column=0)
        self.b_salon.grid(row=1, column=1)
        self.b_sauna.grid(row=1, column=2)

# Bathroom interface
# LED, Contactor, Light (depend of the Pir sensor)
class Bathroom(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.var_led = tk.StringVar()
        self.var_con = tk.StringVar()
        self.var_rel = tk.StringVar()

        self.var_led.set('Off')
        self.var_con.set('Close')
        self.var_rel.set('Off')

        self.l_text = Label(self, text='Bathroom')
        self.l_led = [Label(self, text="LED : "), Label(self, textvariable=self.var_led)]
        self.l_con = [Label(self, text="CONTACTOR : "), Label(self, textvariable=self.var_con)]
        self.l_rel = [Label(self, text="Light : "), Label(self, textvariable=self.var_rel)]
        self.b_retu = Button(self, text='Return', command=lambda p='House': controller.change_page(p))

        self.l_text.grid(row=0, column=0, columnspan=3, pady=(0, 15))
        for i in range(2):
            self.l_led[i].grid(row=1, column=i, pady=(0, 10))
            self.l_con[i].grid(row=2, column=i, pady=(0, 10))
            self.l_rel[i].grid(row=3, column=i, pady=(0, 10))
        self.b_retu.grid(row=4, column=2, padx=(10, 0))

    def changement_variable(self, variable, status):
        if variable == 'LED' and not status:
            self.var_led.set('Off')
        elif variable == 'LED' and status:
            self.var_led.set('Alight')
        elif variable == 'CONTACT' and not status:
            self.var_con.set('Close')
        elif variable == 'CONTACT' and status:
            self.var_con.set('Open')
        elif variable == 'PIR' and status:
            self.var_rel.set('Alight')
        elif variable == 'PIR' and not status:
            self.var_rel.set('Off')

# Bedroom interface
# LED, Contactor, Light
class Bedroom(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.var_led = tk.StringVar()
        self.var_con = tk.StringVar()
        self.var_rel = tk.StringVar()

        self.var_led.set('Off')
        self.var_con.set('Close')
        self.var_rel.set('Off')

        self.l_text = Label(self, text='Bedroom')
        self.l_led = [Label(self, text="LED : "), Label(self, textvariable=self.var_led)]
        self.l_con = [Label(self, text="CONTACTOR : "), Label(self, textvariable=self.var_con)]
        self.l_rel = [Label(self, text="Light : "), Label(self, textvariable=self.var_rel)]
        self.b_retu = Button(self, text='Return', command=lambda p='House': controller.change_page(p))

        self.l_text.grid(row=0, column=0, columnspan=3, pady=(0, 15))
        for i in range(2):
            self.l_led[i].grid(row=1, column=i, pady=(0, 10))
            self.l_con[i].grid(row=2, column=i, pady=(0, 10))
            self.l_rel[i].grid(row=3, column=i, pady=(0, 10))
        self.b_retu.grid(row=4, column=2, padx=(10, 0))

    def changement_variable(self, variable, status):
        if variable == 'LED' and not status:
            self.var_led.set('Off')
        elif variable == 'LED' and status:
            self.var_led.set('Alight')
        elif variable == 'CONTACT' and not status:
            self.var_con.set('Close')
        elif variable == 'CONTACT' and status:
            self.var_con.set('Open')
        elif variable == 'PIR' and status:
            self.var_rel.set('Alight')
        elif variable == 'PIR' and not status:
            self.var_rel.set('Off')

# Garage interface
# LEDs, Motor, Motor_Clockwise, Optical barriere, 
# Button, Lmitie Up, Limite Down
class Garage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.var_led = tk.StringVar()
        self.var_mot = tk.StringVar()
        self.var_clo = tk.StringVar()
        self.var_bar = tk.StringVar()
        self.var_but = tk.StringVar()
        self.var_lim1 = tk.StringVar()
        self.var_lim2 = tk.StringVar()

        self.var_led.set('Off')
        self.var_mot.set('Off')
        self.var_clo.set('True')
        self.var_bar.set('Free')
        self.var_but.set('Released')
        self.var_lim1.set('False')
        self.var_lim2.set('False')

        self.l_text = Label(self, text='Garage')
        self.l_led = [Label(self, text="LEDS : "), Label(self, textvariable=self.var_led)]
        self.l_mot = [Label(self, text="Motor : "), Label(self, textvariable=self.var_mot)]
        self.l_clo = [Label(self, text="Clockwise : "), Label(self, textvariable=self.var_clo)]
        self.l_bar = [Label(self, text="Barriere : "), Label(self, textvariable=self.var_bar)]
        self.l_but = [Label(self, text="Button : "), Label(self, textvariable=self.var_but)]
        self.l_lim1 = [Label(self, text="Switch limit 1 : "), Label(self, textvariable=self.var_lim1)]
        self.l_lim2 = [Label(self, text="Switch limit 2 : "), Label(self, textvariable=self.var_lim2)]
        self.b_retu = Button(self, text='Return', command=lambda p='House': controller.change_page(p))

        self.l_text.grid(row=0, column=0, columnspan=3, pady=(0, 15))
        for i in range(2):
            self.l_led[i].grid(row=1, column=i, pady=(0, 10))
            self.l_mot[i].grid(row=2, column=i, pady=(0, 10))
            self.l_clo[i].grid(row=3, column=i, pady=(0, 10))
            self.l_bar[i].grid(row=4, column=i, padx=(0, 10))
            self.l_but[i].grid(row=5, column=i, pady=(0, 10))
            self.l_lim1[i].grid(row=6, column=i, pady=(0, 10))
            self.l_lim2[i].grid(row=7, column=i, padx=(0, 10))
        self.b_retu.grid(row=8, column=2, padx=(10, 0))

    def changement_variable(self, variable, status):
        if variable == 'LEDS':
            self.var_led.set(status)
        elif variable == 'Motor' and not status:
            self.var_mot.set('Off')
        elif variable == 'Motor' and status:
            self.var_mot.set('On')
        elif variable == 'Clockwise':
            self.var_clo.set(str(status))
        elif variable == 'Barriere' and not status:
            self.var_bar.set('Free')
        elif variable == 'Barriere' and status:
            self.var_bar.set('Breaked')
        elif variable == 'Button' and not status:
            self.var_but.set('Pressed')
        elif variable == 'Button' and status:
            self.var_but.set('Released')
        elif variable == 'Limit_1':
            self.var_lim1.set(str(status))
        elif variable == 'Limit_2':
            self.var_lim2.set(str(status))
        
# Kitchen interface
# LED, Contactor 1, Contactor 2
class Kitchen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.var_led = tk.StringVar()
        self.var_con1 = tk.StringVar()
        self.var_con2 = tk.StringVar()

        self.var_led.set('Off')
        self.var_con1.set('Close')
        self.var_con2.set('Close')

        self.l_text = Label(self, text='Kitchen')
        self.l_led = [Label(self, text="LED : "), Label(self, textvariable=self.var_led)]
        self.l_con1 = [Label(self, text="CONTACTOR 1 : "), Label(self, textvariable=self.var_con1)]
        self.l_con2 = [Label(self, text="CONTACTOR 2 : "), Label(self, textvariable=self.var_con2)]
        self.b_retu = Button(self, text='Return', command=lambda p='House': controller.change_page(p))

        self.l_text.grid(row=0, column=0, columnspan=3)
        for i in range(2):
            self.l_led[i].grid(row=1, column=i, pady=(0, 10))
            self.l_con1[i].grid(row=2, column=i, pady=(0, 10))
            self.l_con2[i].grid(row=3, column=i, pady=(0, 10))
        self.b_retu.grid(row=4, column=2, padx=(10, 0))


    def changement_variable(self, variable, status):
        if variable == 'LED' and not status:
            self.var_led.set('Off')
        elif variable == 'LED' and status:
            self.var_led.set('Alight')
        elif variable == 'CONTACT_1' and not status:
            self.var_con1.set('Close')
        elif variable == 'CONTACT_1' and status:
            self.var_con1.set('Open')
        elif variable == 'CONTACT_2' and not status:
            self.var_con2.set('Close')
        elif variable == 'CONTACT_2' and status:
            self.var_con2.set('Open')

# Salon interface
# LED, Contactor
class Salon(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.var_led = tk.StringVar()
        self.var_con = tk.StringVar()

        self.var_led.set('Off')
        self.var_con.set('Close')

        self.l_text = Label(self, text='Salon')
        self.l_var = [Label(self, text="LED : "), Label(self, textvariable=self.var_led)]
        self.l_con = [Label(self, text="CONTACTOR : "), Label(self, textvariable=self.var_con)]
        self.b_retu = Button(self, text='Return', command=lambda p='House': controller.change_page(p))

        self.l_text.grid(row=0, column=0, columnspan=3)
        for i in range(2):
            self.l_var[i].grid(row=1, column=i, pady=(0, 10))
            self.l_con[i].grid(row=2, column=i, pady=(0, 10))
        self.b_retu.grid(row=3, column=2, padx=(10, 0))

    def changement_variable(self, variable, status):
        if variable == 'LED' and not status:
            self.var_led.set('Off')
        elif variable == 'LED' and status:
            self.var_led.set('Alight')
        elif variable == 'CONTACT' and not status:
            self.var_con.set('Close')
        elif variable == 'CONTACT' and status:
            self.var_con.set('Open')

# Sauna interface
# LED contactor, LED Peltier, Contactor, Peltier, 
# Sensor DHT (Humidity and Temperature)
class Sauna(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.var_led1 = tk.StringVar()
        self.var_led2 = tk.StringVar()
        self.var_con = tk.StringVar()
        self.var_pel = tk.StringVar()
        self.var_temp = tk.StringVar()
        self.var_humi = tk.StringVar()

        self.var_led1.set('Off')
        self.var_led2.set('Not used')
        self.var_con.set('Close')
        self.var_pel.set('Not used')
        self.var_temp.set('')
        self.var_humi.set('')

        self.l_text = Label(self, text='Sauna')
        self.l_var1 = [Label(self, text="LED Contactor : "), Label(self, textvariable=self.var_led1)]
        self.l_var2 = [Label(self, text="LED Peltier : "), Label(self, textvariable=self.var_led2)]
        self.l_con = [Label(self, text="CONTACTOR : "), Label(self, textvariable=self.var_con)]
        self.l_pel = [Label(self, text="PELTIER : "), Label(self, textvariable=self.var_pel)]
        self.l_dht1 = [Label(self, text="Température : "), Label(self, textvariable=self.var_temp)]
        self.l_dht2 = [Label(self, text="Humidity : "), Label(self, textvariable=self.var_humi)]
        self.b_retu = Button(self, text='Return', command=lambda p='House': controller.change_page(p))

        self.l_text.grid(row=0, column=0, columnspan=3)
        for i in range(2):
            self.l_var1[i].grid(row=1, column=i, pady=(0, 10))
            self.l_con[i].grid(row=2, column=i, pady=(0, 10))
            self.l_var2[i].grid(row=3, column=i, pady=(0, 10))
            self.l_pel[i].grid(row=4, column=i, pady=(0, 10))
            self.l_dht1[i].grid(row=5, column=i, pady=(0, 10))
            self.l_dht2[i].grid(row=6, column=i, pady=(0, 10))
        self.b_retu.grid(row=7, column=2, padx=(10, 0))

    def changement_variable(self, variable, status):
        if variable == 'LED' and not status:
            self.var_led1.set('Off')
        elif variable == 'LED' and status:
            self.var_led1.set('Alight')
        elif variable == 'CONTACT' and not status:
            self.var_con.set('Close')
        elif variable == 'CONTACT' and status:
            self.var_con.set('Open')
        elif variable == 'TEMPERATURE':
            self.var_temp.set(f'{status} °C')
        elif variable == 'HUMIDITY':
            self.var_humi.set(f'{status} %')

# Classes to modify to make interface pretty
class Button(tk.Button):
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, font=("Times New Roman", 16), *args, **kwargs)
class Entry(tk.Button):
    def __init__(self, *args, **kwargs):
        tk.Entry.__init__(self, font=("Times New Roman", 16), *args, **kwargs)
class Label(tk.Label):
    def __init__(self, *args, **kwargs):
        tk.Label.__init__(self, font=("Times New Roman", 16), *args, **kwargs)
class Listbox(tk.Listbox):
    def __init__(self, *args, **kwargs):
        tk.Listbox.__init__(self, font=("Times New Roman", 16), *args, **kwargs)
class Checkbutton(tk.Checkbutton):
    def __init__(self, *args, **kwargs):
        tk.Checkbutton.__init__(self, font=("Times New Roman", 16), *args, **kwargs)
        self.onvalue = 1
        self.offvalue = 0
