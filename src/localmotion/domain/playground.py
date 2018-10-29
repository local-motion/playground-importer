from src.localmotion.domain.address import Address


class Playground:
    def __init__(self, id_: str, name: str, address: Address, type_: str, status: str, website: str) -> None:
        self.initiativeId = id_
        self.name = name
        self.address = address
        self.type = "smokefree"
        self.status = "finished"
        self.website = website
