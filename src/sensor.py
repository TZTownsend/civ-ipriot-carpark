import random
from abc import ABC, abstractmethod


class Sensor(ABC):
    def __init__(self, id, is_active=False, car_park):
        self.id = id
        self.is_active = is_active
        self.car_park = car_park

    @abstractmethod
    def update_car_park(self, plate):
        pass

    def _scan_plate(self):
        # return random plate id
        return "PRJ-" + format(random.randint(0, 999), "03d")

    def detect_vehicle(self):
        plate = self._scan_plate()
        self.update_car_park(plate)


class EntrySensor(Sensor):
    def update_car_park(self, plate):
        print(f"Incoming 🚘 vehicle detected. Plate: {plate}")
        self.car_park.add_car(plate)


class ExitSensor(Sensor):
    def _scan_plate(self):
        # return random plate from car park plates
        return random.choice(self.car_park.plates)

    def update_car_park(self, plate):
        print(f"Outgoing 🚗 vehicle detected. Plate: {plate}")
        self.car_park.remove_car(plate)
