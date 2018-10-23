from src.localmotion.domain.address import Address


class Playground:
    def __init__(self, id_: str, title: str, address: Address, type_: str, status: str, website: str) -> None:
        self.id = id_
        self.title = title
        self.address = address
        self.type = type_
        self.status = status
        self.website = website


