import unittest
from display import Display
from car_park import CarPark


class TestCarPark(unittest.TestCase):
    def setUp(self):
        self.display = Display(id=1,
                               message="Welcome to the car park",
                               is_on=True,
                               car_park=CarPark(location="123 Test St",
                                                capacity=100,
                                                temperature=22))

    def test_display_initialised_with_all_attributes(self):
        self.assertIsInstance(self.display, Display)
        self.assertEqual(self.display.id, 1)
        self.assertIsInstance(self.display.car_park, CarPark)
        self.assertEqual(self.display.message, {"Message": "Welcome to the car park"})
        self.assertEqual(self.display.is_on, True)

    def test_update(self):
        self.display.update({"Message": "Goodbye"})
        self.assertTrue("Goodbye", self.display.message.get("Message"))


if __name__ == "__main__":
    unittest.main()
