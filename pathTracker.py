from kivy.garden.mapview import MapMarkerPopup, MapMarker
import myMapView
from lineLayer import LineLayer
from skspatial.objects import Line
from skspatial.objects import Points
from skspatial.plotting import plot_3d

'''
pip install scikit-spatial
'''


class PathTracker:
    def __init__(self, line_layer, **kwargs):
        self.points = []
        self.apogee_nr = None
        self.line_layer: LineLayer = line_layer
        self.height_label = None
        self.initial_alt = None
        self.mapview = None
        self.map_marker = None
        self.max_alt = -10

    def add_point(self, point, alt=None):
        if self.initial_alt is None:
            self.initial_alt = alt
        self.points.append((point[0], point[1], alt))
        self.line_layer.coordinates.append(point)
        self.line_layer.reposition()
        if alt is not None:
            self.height_label.text = 'UFO Height: ' + str(alt) + 'm; from the start point:' + str(
                alt - self.initial_alt) + 'm'
            self.max_alt = max(self.max_alt, alt)
            if alt < self.max_alt and self.apogee_nr is not None and len(self.points[self.apogee_nr:]) > 1:
                print()
                line = Line.best_fit(self.points[self.apogee_nr:])
                line_t = (self.initial_alt - line.point[2]) / line.vector[2]
                lat = line.point[0] + line_t * line.vector[0]
                lon = line.point[1] + line_t * line.vector[1]
                if self.map_marker is not None:
                    self.mapview.remove_marker(self.map_marker)
                self.map_marker = MapMarker(lat=float(lat), lon=float(lon), source='resources/predicted_fall.png',
                                            size=(0.5, 0.05), size_hint=(0.00005, 0.00005),
                                            allow_stretch=True, anchor_x=0.5, anchor_y=0.5)
                self.mapview.add_marker(self.map_marker)
            if alt < self.max_alt and self.apogee_nr is None:
                self.apogee_nr = len(self.points)
