from kivy.garden.mapview import MapView, MapMarkerPopup, MapMarker
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout


class PathTracker:
    def __init__(self, lineLayer, **kwargs):
        self.points = []
        self.lineLayer = lineLayer

    def add_point(self, point):
        self.points.append(point)
        self.lineLayer.coordinates = [self.points[0], self.points[-1]]

