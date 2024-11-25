class Display:
    def __init__(self, id, car_park, message="", is_on=False):
        self.id = id
        self.message = {"Message": message}
        self.is_on = is_on
        self.car_park = car_park

    def __str__(self):
        return f"Display {self.id}: {self.message}"

    def update(self, data: dict):
        """
        Outputs message data to displays.
        :param data:
        :return:
        """
        self.message.update(data)
        if self.is_on:
            print("=" * 50)
            for key, value in data.items():
                print(f"{key}: {value}")
            print(("=" * 50), "\n")
