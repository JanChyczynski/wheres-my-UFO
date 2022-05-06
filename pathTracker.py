from kivy.garden.mapview import MapView, MapMarkerPopup, MapMarker
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout


class PathTracker:
    def __init__(self, line_layer, **kwargs):
        self.points = []
        self.line_layer = line_layer

    def add_point(self, point):
        self.points.append(point)
        self.line_layer.coordinates = [self.points[0], self.points[-1]]

