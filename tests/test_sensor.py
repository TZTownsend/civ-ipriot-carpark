import unittest
from sensor import Sensor, EntrySensor, ExitSensor
from car_park import CarPark


class MockCarPark:
    def __init__(self, *args, **kwargs):
        self.plates = []

    def add_car(self, plate):
        self.plates.append(plate)

    def remove_car(self, plate):
        self.plates.pop()


class TestEntrySensor(unittest.TestCase):
    def setUp(self):
        self.entry_sensor = EntrySensor(id=123, car_park=MockCarPark())

    def test_entry_sensor_initialised_with_all_attributes(self):
        self.assertIsInstance(self.entry_sensor, EntrySensor)
        self.assertEqual(self.entry_sensor.id, 123)
        self.assertIsInstance(self.entry_sensor.car_park, MockCarPark)
        self.assertEqual(self.entry_sensor.is_active, False)

    def test_detect_vehicle(self):
        self.entry_sensor.detect_vehicle()
        self.assertEqual(len(self.entry_sensor.car_park.plates), 1)


class TestExitSensor(unittest.TestCase):
    def setUp(self):
        self.exit_sensor = ExitSensor(id=456, car_park=MockCarPark())

    def test_exit_sensor_initialised_with_all_attributes(self):
        self.assertIsInstance(self.exit_sensor, ExitSensor)
        self.assertEqual(self.exit_sensor.id, 456)
        self.assertIsInstance(self.exit_sensor.car_park, MockCarPark)
        self.assertEqual(self.exit_sensor.is_active, False)

    def test_detect_vehicle(self):
        self.exit_sensor.car_park.plates = ["TEST-001", "TEST-002", "TEST-003"]
        self.exit_sensor.detect_vehicle()
        self.assertEqual(len(self.exit_sensor.car_park.plates), 2)


if __name__ == "__main__":
    unittest.main()
