from sensor import Sensor
from display import Display


class CarPark:
    def __init__(self, location='Unknown', capacity=0, plates=None,
                 sensors=None, displays=None):
        self.location = location
        self.capacity = capacity
        self.plates = plates or []
        self.sensors = sensors or []
        self.displays = displays or []

    def __str__(self):
        return f"Car park at {self.location}, with {self.capacity} bays."

    def register(self, component):
        if not isinstance(component, (Sensor, Display)):
            raise TypeError("Object must be a Sensor or Display")
        if isinstance(component, Sensor):
            self.sensors.append(component)
        elif isinstance(component, Display):
            self.displays.append(component)

    def add_car(self, plate):
        self.plates.append(plate)
        self.update_displays()

    def remove_car(self, plate):
        try:
            self.plates.remove(plate)
        except ValueError:
            # code to deal with undetected plates
            self.plates.pop()
        self.update_displays()

