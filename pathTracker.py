from kivy.garden.mapview import MapView, MapMarkerPopup, MapMarker
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from lineLayer import LineLayer


class PathTracker:
    def __init__(self, line_layer, **kwargs):
        self.points = []
        self.line_layer: LineLayer = line_layer
        self.height_label = None

    def add_point(self, point, alt=None):
        self.points.append((point[0], point[1], alt))
        print(self.line_layer.coordinates)
        self.line_layer.coordinates.append(point)
        self.line_layer.reposition()
        if alt is not None:
            self.height_label.text = 'UFO Height: '+str(alt)
