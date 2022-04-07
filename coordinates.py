class Coords:
    def __init__(self, latitude, longitude, altitude):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    @classmethod
    def from_dict(cls, data):
        return cls(data["latitude"], data["longitude"], data["altitude"])

    def __str__(self):
        return f"latitude: {self.latitude}, longitude: {self.longitude}, alt: {self.altitude}"
