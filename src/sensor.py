import random
from abc import ABC, abstractmethod


class Sensor(ABC):
    def __init__(self, id, car_park, is_active=False):
        self.id = id
        self.is_active = is_active
        self.car_park = car_park

    @abstractmethod
    def update_car_park(self, plate):
        """
        Updates CarPark plates list by appending or removing number plate id.
        :param plate:
        :return:
        """
        pass

    def _scan_plate(self):
        """
        Simulates a number plate scanner to return a random plate id.
        :return:
        """
        # return random plate id
        return "PRJ-" + format(random.randint(0, 999), "03d")

    def detect_vehicle(self):
        """
        When vehicle is detected by a sensor the number plate is scanned and
        the CarPark is updated with the plate information.
        :return:
        """
        plate = self._scan_plate()
        self.update_car_park(plate)


class EntrySensor(Sensor):
    def update_car_park(self, plate):
        print(f"Incoming 🚘 vehicle detected. Plate: {plate}")
        self.car_park.add_car(plate)


class ExitSensor(Sensor):
    def _scan_plate(self):
        """
        Simulates a plate scanner by returning a plate id that has been
        previously scanned into the carpark.
        :return:
        """
        # return random plate from car park plates
        return random.choice(self.car_park.plates)

    def update_car_park(self, plate):
        print(f"Outgoing 🚗 vehicle detected. Plate: {plate}")
        self.car_park.remove_car(plate)
