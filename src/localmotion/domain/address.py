class Address:
    def __init__(self, street: str, number: int, zipcode: str, city: str) -> None:
        self.street = street
        self.number = number
        self.zipcode = zipcode
        self.city = city

    def to_readable_address(self):
        return "{} {}, {}, {}, Nederland".format(self.street, self.number, self.zipcode, self.city)
