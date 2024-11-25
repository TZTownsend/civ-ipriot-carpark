import json
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
                 log_file=Path("log.txt"),
                 config_file=Path("config.json")):
        self.location = location
        self.capacity = capacity
        self.temperature = temperature
        self.plates = plates or []
        self.sensors = sensors or []
        self.displays = displays or []
        self.log_file = log_file if isinstance(log_file, Path) else Path(
            log_file)
        self.log_file.touch(exist_ok=True)
        self.config_file = config_file if isinstance(config_file, Path) else Path(
            config_file)

    @property
    def available_bays(self):
        """
        Dynamically calculates available bays in carpark.
        :return:
        """
        return max(0, self.capacity - len(self.plates))

    @classmethod
    def from_config(cls, config_file=Path("config.json")):
        """
        Enables instantiation of a CarPark from a JSON configuration file.
        :param config_file:
        :return:
        """
        config_file = config_file if isinstance(config_file, Path) else Path(
            config_file)
        with config_file.open() as f:
            config = json.load(f)
        return cls(location=config["location"], capacity=config["capacity"],
                   log_file=config["log_file"])

    def update_temperature(self, temperature):
        """
        Updates temperature at carpark location and sends new data to carpark
        displays.
        :param temperature:
        :return:
        """
        self.temperature = temperature
        self.update_displays()

    def __str__(self):
        return f"Car park at {self.location}, with {self.capacity} bays."

    def register(self, component):
        """
        Registers carpark components (eg Sensors and Displays). Components
         are set to on when they are registered to the carpark.
        :param component:
        :return:
        """
        if not isinstance(component, (Sensor, Display)):
            raise TypeError("Object must be a Sensor or Display")
        if isinstance(component, Sensor):
            component.is_active = True
            self.sensors.append(component)
        elif isinstance(component, Display):
            component.is_on = True
            self.displays.append(component)

    def deregister(self, component):
        """
        Removes carpark components from the CarPark.
        :param component:
        :return:
        """
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
        """
        Adds car number plate to plates list and sends updated information
        to Displays for output.  Logs number plate as entered in log file.
        :param plate:
        :return:
        """
        self.plates.append(plate)
        self.update_displays()
        self._log_car_activity(plate, action="entered")

    def remove_car(self, plate):
        """
        Removes car numberplate from list of plates in carpark and sends
        update to displays. Logs number plate as exited in log file.
        :param plate:
        :return:
        """
        if len(self.plates) > 0:
            try:
                self.plates.remove(plate)
            except ValueError:
                # code to deal with undetected plates
                self.plates.pop()
            self.update_displays()
            self._log_car_activity(plate, action="exited")

    def update_displays(self):
        """
        Sends updated information to carpark displays.
        :return:
        """
        for display in self.displays:
            display.update({"Available_bays": self.available_bays,
                            "Temperature": self.temperature})

    def _log_car_activity(self, plate, action):
        """
        Writes car activity data to log file.
        :param plate:
        :param action:
        :return:
        """
        with self.log_file.open("a") as f:
            f.write(
                f"{plate} {action} at {datetime.now():%Y-%m-%d %H:%M:%S}\n")

    def write_config(self):
        """
        Writes configuration data to configuration file.
        :return:
        """
        with open(self.config_file, "w") as f:
            json.dump({"location": self.location,
                       "capacity": self.capacity,
                       "log_file": str(self.log_file)}, f)
