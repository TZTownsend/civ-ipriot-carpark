from pathlib import Path
from datetime import datetime
from sensor import Sensor
from display import Display


class CarPark:
    def __init__(self,
                 location="Unknown",
                 capacity=0,
                 temperature="Unknown",
                 plates=None,
                 sensors=None,
                 displays=None,
                 log_file=Path("log.txt")):
        self.location = location
        self.capacity = capacity
        self.temperature = temperature
        self.plates = plates or []
        self.sensors = sensors or []
        self.displays = displays or []
        self.log_file = log_file if isinstance(log_file, Path) else Path(
            log_file)
        self.log_file.touch(exist_ok=True)

    @property
    def available_bays(self):
        return max(0, self.capacity - len(self.plates))

    def update_temperature(self, temperature):
        self.temperature = temperature
        self.update_displays()

    def __str__(self):
        return f"Car park at {self.location}, with {self.capacity} bays."

    def register(self, component):
        if not isinstance(component, (Sensor, Display)):
            raise TypeError("Object must be a Sensor or Display")
        if isinstance(component, Sensor):
            self.sensors.append(component)
        elif isinstance(component, Display):
            self.displays.append(component)

    def deregister(self, component):
        if not isinstance(component, (Sensor, Display)):
            raise TypeError("Object must be a Sensor or Display")
        if isinstance(component, Sensor):
            try:
                self.sensors.remove(component)
            except:
                raise ValueError("Sensor not found")
        elif isinstance(component, Display):
            try:
                self.displays.remove(component)
            except:
                raise ValueError("Display not found")

    def add_car(self, plate):
        self.plates.append(plate)
        self.update_displays()
        self._log_car_activity(plate, action="entered")

    def remove_car(self, plate):
        if len(self.plates) > 0:
            try:
                self.plates.remove(plate)
            except ValueError:
                # code to deal with undetected plates
                self.plates.pop()
            self.update_displays()
            self._log_car_activity(plate, action="exited")

    def update_displays(self):
        for display in self.displays:
            display.update({"Available_bays": self.available_bays,
                            "Temperature": self.temperature})

    def _log_car_activity(self, plate, action):
        with self.log_file.open("a") as f:
            f.write(
                f"{plate} {action} at {datetime.now():%Y-%m-%d %H:%M:%S}\n")
