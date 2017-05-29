from RPi import GPIO as io

class Button(object):


    def __init__(self, input_pin, name="Button", pull_up_down=io.PUD_DOWN):
        self.input_pin = input_pin
        self.name = name
        self.type = pull_up_down

    def set_callback(self, callback_function):
        self.callback_function = callback_function

    def setup(self):
        io.setmode(io.BCM)
        io.setup(self.input_pin, io.IN, pull_up_down=self.type)
        io.add_event_detect(self.input_pin, io.RISING)
        io.add_event_callback(self.input_pin, self.__handle_callback)

    def value(self):
        return io.input(self.input_pin)

    def cleanup(self):
        io.cleanup((self.input_pin))
    
    def __handle_callback(self, pin):
        if pin == self.input_pin and self.callback_function:
            self.callback_function()
