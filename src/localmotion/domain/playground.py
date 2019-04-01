from src.localmotion.domain.address import Address
from src.localmotion.domain.geo_location import GeoLocation


class Playground:
    # def __init__(self, id_: str, name: str, address: Address, geo_location: GeoLocation, type_: str, status: str, website: str) -> None:
    def __init__(self, id_: str, name: str, creationStatus: str, geo_location: GeoLocation) -> None:
        self.initiativeId = id_
        self.name = name
        self.creationStatus = creationStatus
        # self.address = address
        self.geoLocation = geo_location
        # self.type = type_
        # self.status = status
        # self.website = website
