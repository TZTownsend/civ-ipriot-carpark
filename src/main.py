from car_park import CarPark
from display import Display
from sensor import EntrySensor, ExitSensor


def main():
    car_park = CarPark(location="moondalup",
                       capacity=100,
                       log_file="moondalup.txt")

    entry_sensor = EntrySensor(id=1,
                               is_active=True,
                               car_park=car_park)

    exit_sensor = ExitSensor(id=2,
                             is_active=True,
                             car_park=car_park)

    display = Display(id=1,
                      is_on=True,
                      car_park=car_park,
                      message="Welcome to Moondalup")

    car_park.register(entry_sensor)
    car_park.register(exit_sensor)
    car_park.register(display)

    for i in range(10):
        entry_sensor.detect_vehicle()

    for i in range(2):
        exit_sensor.detect_vehicle()


if __name__ == "__main__":
    main()