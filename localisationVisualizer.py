from kivy.garden.mapview import MapView, MapMarkerPopup, MapMarker
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

from azimuthVisualizer import AzimuthVisualizer
from lineLayer import LineLayer
from pathTracker import PathTracker
from saveDialog import SaveUFODialog, SaveUserDialog

Builder.load_file('localisationVisualiser.kv')


class LocalisationVisualizer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.save_UFO_popup = SaveUFODialog(self)
        self.save_user_popup = SaveUserDialog(self)
        self._lineLayer = LineLayer(coordinates=[[0, 0], [0, 0]])
        self._layer_added = False
        self.pathTracker = PathTracker(self._lineLayer)
        self.azimuthVisualizer = AzimuthVisualizer()
        Clock.schedule_once(self.pass_kivy_values,0.05)

    def pass_kivy_values(self, *args):
        self.azimuthVisualizer.mapview = self.ids.map_view
        self.azimuthVisualizer.text_label = self.ids.azimuth_label

    def enter_user_coordinates(self):
        self.save_user_popup.open()

    def enter_UFO_coordinates(self):
        self.save_UFO_popup.open()

    def add_user_coordinates(self, lat, lon):
        self.add_user_marker(lat, lon)

    def add_UFO_coordinates(self, lat, lon):
        self.add_UFO_marker(lat, lon)
        self.pathTracker.add_point((lat, lon))

    def add_UFO_marker(self, lat, lon):
        if not self._layer_added:
            self.ids.map_view.add_layer(self._lineLayer, mode="scatter")
            self._layer_added = True
        self.azimuthVisualizer.set_UFO_pos((lat, lon))
        marker = MapMarker(lat=lat, lon=lon, source='alien100.png', size=(1, 0.1), size_hint=(None, None),
                           allow_stretch=True)
        self.ids.map_view.add_marker(marker)

    def add_user_marker(self, lat, lon):
        if not self._layer_added:
            self.ids.map_view.add_layer(self._lineLayer, mode="scatter")
            self._layer_added = True
        self.azimuthVisualizer.set_user_marker(MapMarker(lat=lat, lon=lon, source='user_location.png',
                                                       size=(1, 0.1), size_hint=(0.0001, 0.0001), allow_stretch=True))
        self.azimuthVisualizer.update_user_marker([lat, lon])
