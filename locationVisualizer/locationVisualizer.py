from kivy.garden.mapview import MapMarker
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

from locationVisualizer.azimuthVisualizer import AzimuthVisualizer
from locationVisualizer.coordsReceiver import CoordinatesReceiver
from locationVisualizer.lineLayer import LineLayer
from locationVisualizer.pathTracker import PathTracker
from saveDialog import SaveUFODialog, SaveUserDialog

Builder.load_file('locationVisualizer/locationVisualiser.kv')


class LocationVisualizer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.save_UFO_popup = SaveUFODialog(self)
        self.save_user_popup = SaveUserDialog(self)
        self._lineLayer = LineLayer(coordinates=[])
        self._layer_added = False
        self.pathTracker = PathTracker(self._lineLayer)
        self.azimuthVisualizer = AzimuthVisualizer()
        self.receiver = None
        self.prev_marker = None
        Clock.schedule_once(self.pass_kivy_values, 0.05)

    def pass_kivy_values(self, *args):
        self.azimuthVisualizer.mapview = self.ids.map_view
        self.azimuthVisualizer.azimuth_label = self.ids.azimuth_label
        self.pathTracker.height_label = self.ids.height_label
        self.pathTracker.mapview = self.ids.map_view

    def enter_user_coordinates(self):
        self.save_user_popup.open()

    def enter_UFO_coordinates(self):
        self.save_UFO_popup.open()

    def add_user_coordinates(self, lat, lon):
        self.add_user_marker(lat, lon)

    def add_UFO_coordinates(self, lat, lon, alt=None):
        self.add_UFO_marker(lat, lon)
        self.pathTracker.add_point((lat, lon), alt)

    def start_receiving(self, ip, port):
        if self.receiver is not None:
            self.receiver.close()
            del self.receiver
        self.receiver = CoordinatesReceiver(ip, port)
        Clock.schedule_interval(self.handle_receive, 1)

    def handle_receive(self, *args):
        coords = self.receiver.receive()
        if coords is not None:
            self.add_UFO_coordinates(coords.latitude, coords.longitude, coords.altitude)

    def add_UFO_marker(self, lat, lon):
        if not self._layer_added:
            self.ids.map_view.add_layer(self._lineLayer, mode="scatter")
            self._layer_added = True
        self.azimuthVisualizer.set_UFO_pos((lat, lon))
        if self.prev_marker is not None:
            self.ids.map_view.remove_marker(self.prev_marker)
        marker = MapMarker(lat=lat, lon=lon, source='resources/ufo.png', size=(1, 0.1), size_hint=(None, None),
                           allow_stretch=True, anchor_x=0.5, anchor_y=0.5)
        self.ids.map_view.add_marker(marker)
        self.prev_marker = marker

    def add_user_marker(self, lat, lon):
        if not self._layer_added:
            self.ids.map_view.add_layer(self._lineLayer, mode="scatter")
            self._layer_added = True
        self.azimuthVisualizer.remove_user_marker()
        self.azimuthVisualizer.user_marker = MapMarker(lat=lat, lon=lon, source='resources/user_location.png',
                                                       size=(1, 0.1), size_hint=(0.0001, 0.0001),
                                                       allow_stretch=True)
        self.azimuthVisualizer.update_user_marker([lat, lon])
