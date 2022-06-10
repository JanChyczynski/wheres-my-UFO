from math import atan, pi

from kivy.garden.mapview import MapView, MapMarkerPopup, MapMarker
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from numpy import rad2deg, arctan2

from lineLayer import LineLayer


class AzimuthVisualizer:
    def __init__(self, **kwargs):
        self.user_marker = None
        self.user_pos = None
        self.mapview = None
        self.line_layer = None
        self.UFO_pos = None
        self.azimuth_label = None

    def _set_line_layer(self):
        if self.line_layer is None and self.UFO_pos is not None and self.user_pos is not None:
            self.line_layer = LineLayer(coordinates=[self.UFO_pos, self.user_pos], color=[1, 0, 0, 1])
            self.mapview.add_layer(self.line_layer, mode='scatter')

    def set_UFO_pos(self, UFO_pos):
        self._set_line_layer()
        self.UFO_pos = UFO_pos
        if self.user_pos is not None and self.line_layer is not None:
            self.line_layer.coordinates = [self.UFO_pos, self.user_pos]
            self.calc_azimuth()

    def calc_azimuth(self):
        azimuth = (rad2deg(
            arctan2((-self.user_pos[1] + self.UFO_pos[1]), (-self.user_pos[0] + self.UFO_pos[0])) + pi) + 180) % 360
        self.azimuth_label.text = "Azimuth: " + str(azimuth)

    def remove_user_marker(self):
        if self.user_marker is not None:
            self.mapview.remove_marker(self.user_marker)

    def update_user_marker(self, user_pos):
        self.user_pos = user_pos
        self._set_line_layer()
        if self.UFO_pos is not None:
            self.line_layer.coordinates = [self.UFO_pos, self.user_pos]
            self.calc_azimuth()
        self.mapview.add_marker(self.user_marker)
        if self.line_layer is not None:
            self.line_layer.reposition()

