from kivy_garden.mapview import MapMarker, MapView

from main import MapViewApp


class SignalMarker:
    def __init__(self, lat, lon, strength, map_view: MapView):
        self.lat = lat
        self.lon = lon
        self.strength = strength
        self.center_marker = MapMarker(lat=lat, lon=lon, source=MapViewApp.CENTER_MARKER_SRC)
        self.center_marker.size = [30, 30]
        self.center_marker.anchor_y = 0.5
        map_view.add_marker(self.center_marker)
        self.signal_marker = MapMarker(lat=lat, lon=lon, source=MapViewApp.SIGNAL_MARKER_SRC)
        self.signal_marker.anchor_y = 0.5
        self.update_signal_marker(1)
        map_view.add_marker(self.signal_marker)

    def update_signal_marker(self, ratio):
        self.signal_marker.size = [10 * self.strength * ratio, 10 * self.strength * ratio]
        self.signal_marker.lat = self.lat
        self.signal_marker.lon = self.lon
        self.signal_marker.anchor_y = .5
        self.signal_marker.anchor_x = .5
