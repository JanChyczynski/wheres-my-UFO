import random
import threading
from datetime import datetime

from kivy.clock import Clock
from kivy.garden.mapview import MapView, MapMarkerPopup, MapMarker, MapLayer
from kivy.graphics import Color, Line, Rectangle
from kivy.graphics.context_instructions import Translate, Scale, PushMatrix, PopMatrix
from mapview.utils import clamp
from mapview import \
    (MIN_LONGITUDE, MAX_LONGITUDE, MIN_LATITUDE, MAX_LATITUDE)
from math import radians, log, tan, cos, pi

from probabilityCalculator import ProbabiltyCalculator

"""whole class taken from:
https://github.com/kivy-garden/mapview/issues/4"""


class HeatmapLayer(MapLayer):
    max_opacity = 0.6
    try_reposition_interval = 0.05
    move_cooldown = 0.05

    def __init__(self, probab_claculator: ProbabiltyCalculator, color=[0, 0, 1, 0.5], resolution: int = 45, **kwargs):
        super().__init__(**kwargs)
        # self.calc_coordinates()
        self.probab_calculator = probab_claculator
        self._coordinates = [[0, 0]]
        self.color = color
        self.colors = []
        self._points = None
        self._points_offset = (0, 0)
        self.resolution = resolution
        self.zoom = 0
        self.lon = 0
        self.lat = 0
        self.ms = 0
        self.rng = random.Random()

        Clock.schedule_interval(self.timed_reposition, HeatmapLayer.try_reposition_interval)
        self.moved = False
        self.moved_time = datetime.now()

    def calc_coordinates(self):
        bbox = self.parent.get_bbox()
        top_left = [bbox[0], bbox[1]]
        bottom_right = [bbox[2], bbox[3]]
        step_x = (bbox[2] - bbox[0]) / self.resolution
        step_y = (bbox[3] - bbox[1]) / self.resolution
        self._coordinates = []
        for i in range(self.resolution):
            for j in range(self.resolution):
                self.coordinates.append([top_left[0] + j * step_x, top_left[1] + i * step_y])

        self.colors = [
            self.color[:-1] + [self.probab_calculator.get_probab_manual(lat, lon,
                                                                        self.parent.parent.ids.slider.value) * HeatmapLayer.max_opacity]
            for
            lat, lon in self.coordinates]
        # self.coordinates = [[bbox[0], bbox[3]], [bbox[2], bbox[1]]]

        # self.coordinates = self._coordinates

    @property
    def coordinates(self):
        return self._coordinates

    @coordinates.setter
    def coordinates(self, coordinates):
        self._coordinates = coordinates
        self.invalidate_points()
        self.clear_and_redraw()

    @property
    def points(self):
        if self._points is None:
            self.calc_points()
        return self._points

    @property
    def points_offset(self):
        if self._points is None:
            self.calc_points()
        return self._points_offset

    def calc_points(self):
        # Offset all points by the coordinates of the first point,
        # to keep coordinates closer to zero.
        # (and therefore avoid some float precision issues when drawing lines)
        self._points_offset = (self.get_x(self.coordinates[0][1]),
                               self.get_y(self.coordinates[0][0]))
        # Since lat is not a linear transform we must compute manually
        self._points = [(self.get_x(lon) - self._points_offset[0],
                         self.get_y(lat) - self._points_offset[1])
                        for lat, lon in self.coordinates]

    def invalidate_points(self):
        self._points = None
        self._points_offset = (0, 0)

    def get_x(self, lon):
        """Get the x position on the map using this map source's projection
        (0, 0) is located at the top left.
        """
        return clamp(lon, MIN_LONGITUDE, MAX_LONGITUDE) * self.ms / 360.0

    def get_y(self, lat):
        """Get the y position on the map using this map source's projection
        (0, 0) is located at the top left.
        """
        lat = radians(clamp(-lat, MIN_LATITUDE, MAX_LATITUDE))
        return (1.0 - log(tan(lat) + 1.0 / cos(lat)) / pi) * self.ms / 2.0

    def reposition(self):
        self.moved = True
        self.moved_time = datetime.now()

    # Function called when the MapView is moved
    def timed_reposition(self, ignored):
        # print("try reposition")
        map_view = self.parent
        time_diff = (datetime.now() - self.moved_time).total_seconds()
        if map_view is None or self.moved is False or \
                time_diff < HeatmapLayer.move_cooldown:
            return
        print("reposition", time_diff)
        self.calc_coordinates()
        # Must redraw when the zoom changes
        # as the scatter transform resets for the new tiles
        self.calc_points()

        if self.zoom != map_view.zoom or \
                self.lon != round(map_view.lon, 7) or \
                self.lat != round(map_view.lat, 7):
            map_source = map_view.map_source
            self.ms = pow(2.0, map_view.zoom) * map_source.dp_tile_size
            self.invalidate_points()
            self.clear_and_redraw()
        self.moved = False

    def clear_and_redraw(self, *args):
        with self.canvas:
            # Clear old line
            self.canvas.clear()

        self._draw()

    def _draw(self, *args):
        map_view = self.parent
        self.zoom = map_view.zoom
        self.lon = map_view.lon
        self.lat = map_view.lat

        # When zooming we must undo the current scatter transform
        # or the animation distorts it
        scatter = map_view._scatter
        sx, sy, ss = scatter.x, scatter.y, scatter.scale

        # Account for map source tile size and map view zoom
        vx, vy, vs = map_view.viewport_pos[0], map_view.viewport_pos[1], map_view.scale

        with self.canvas:
            # Save the current coordinate space context
            PushMatrix()

            # Offset by the MapView's position in the window (always 0,0 ?)
            Translate(*map_view.pos)

            # Undo the scatter animation transform
            Scale(1 / ss, 1 / ss, 1)
            Translate(-sx, -sy)

            # Apply the get window xy from transforms
            Scale(vs, vs, 1)
            Translate(-vx, -vy)

            # Apply what we can factor out of the mapsource long, lat to x, y conversion
            Translate(self.ms / 2, 0)

            # Translate by the offset of the line points
            # (this keeps the points closer to the origin)
            Translate(*self.points_offset)

            # print("draw", self.points, self.points[0])
            self.add_shape()

            # Retrieve the last saved coordinate space context
            PopMatrix()

    def add_shape(self):
        # Rectangle(pos=self.points[0], size=[-1000, 1000])
        for (x, y), color in zip(self.points, self.colors):
            if color[-1] < 0.05:
                continue
            Color(*color)
            Rectangle(pos=[x, y], size=[self.parent.size[0] / self.resolution,
                                        self.parent.size[1] / self.resolution])
