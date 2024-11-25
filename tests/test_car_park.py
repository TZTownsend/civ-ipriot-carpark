from pathlib import Path
import unittest
from car_park import CarPark


class TestCarPark(unittest.TestCase):
    def setUp(self):
        self.car_park = CarPark(location="123 Example Street",
                                capacity=100,
                                temperature=22)
        self.new_car_park = CarPark(location="123 Example Street",
                                    capacity=100,
                                    log_file="new_log.txt")

    def test_car_park_initialized_with_all_attributes(self):
        self.assertIsInstance(self.car_park, CarPark)
        self.assertEqual(self.car_park.location, "123 Example Street")
        self.assertEqual(self.car_park.capacity, 100)
        self.assertEqual(self.car_park.temperature, 22)
        self.assertEqual(self.car_park.plates, [])
        self.assertEqual(self.car_park.sensors, [])
        self.assertEqual(self.car_park.displays, [])
        self.assertEqual(self.car_park.available_bays, 100)
        self.assertEqual(self.car_park.log_file, Path("log.txt"))

    def test_log_file_created(self):
        self.assertTrue(Path(self.new_car_park.log_file).exists())

    def tearDown(self):
        Path(self.new_car_park.log_file).unlink(missing_ok=True)

    def test_car_logged_when_entering(self):
        self.car_park.add_car("NEW-001")
        with self.car_park.log_file.open() as f:
            last_line = f.readlines()[-1]
        self.assertIn("NEW-001", last_line)  # check plate entered
        self.assertIn("entered", last_line)  # check description
        self.assertIn("\n", last_line)  # check entry has a new line

    def test_car_logged_when_exiting(self):
        self.car_park.add_car("NEW-001")
        self.car_park.remove_car("NEW-001")
        with self.car_park.log_file.open() as f:
            last_line = f.readlines()[-1]
        self.assertIn("NEW-001", last_line)  # check plate entered
        self.assertIn("exited", last_line)  # check description
        self.assertIn("\n", last_line)  # check entry has a new line

    def test_car_park_update_temperature(self):
        self.car_park.update_temperature(28)
        self.assertEqual(self.car_park.temperature, 28)

    def test_add_car(self):
        self.car_park.add_car("FAKE-001")
        self.assertEqual(self.car_park.plates, ["FAKE-001"])
        self.assertEqual(self.car_park.available_bays, 99)

    def test_remove_car(self):
        self.car_park.add_car("FAKE-001")
        self.car_park.remove_car("FAKE-001")
        self.assertEqual(self.car_park.plates, [])
        self.assertEqual(self.car_park.available_bays, 100)

    def test_overfill_the_car_park(self):
        for i in range(100):
            self.car_park.add_car(f"FAKE-{i}")
        self.assertEqual(self.car_park.available_bays, 0)
        self.car_park.add_car("FAKE-100")
        # Overfilling the car park should not change the number of available bays
        self.assertEqual(self.car_park.available_bays, 0)

        # Removing a car from an overfilled car park should not change the number of available bays
        self.car_park.remove_car("FAKE-100")
        self.assertEqual(self.car_park.available_bays, 0)

    def test_removing_a_car_that_does_not_exist(self):
        self.car_park.add_car("TEST-111")
        self.car_park.remove_car("NO-1")
        self.assertEqual(self.car_park.plates, [])
        self.assertEqual(self.car_park.available_bays, 100)

    def test_register_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.car_park.register("Not a Sensor or Display")

    def test_carpark_can_be_initialised_with_config_file(self):
        self.car_park.location = "1 Config St"
        self.car_park.write_config()
        carpark_from_config_file = CarPark.from_config()
        self.assertIsInstance(carpark_from_config_file, CarPark)
        self.assertEqual(carpark_from_config_file.location, "1 Config St")
        self.assertEqual(carpark_from_config_file.capacity, 100)
        self.assertEqual(carpark_from_config_file.temperature, "Unknown")
        self.assertEqual(carpark_from_config_file.plates, [])
        self.assertEqual(carpark_from_config_file.sensors, [])
        self.assertEqual(carpark_from_config_file.displays, [])
        self.assertEqual(carpark_from_config_file.available_bays, 100)
        self.assertEqual(carpark_from_config_file.log_file, Path("log.txt"))


if __name__ == "__main__":
    unittest.main()
