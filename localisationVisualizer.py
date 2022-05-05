from kivy.garden.mapview import MapView, MapMarkerPopup, MapMarker
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

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

    def enter_user_coordinates(self):
        self.save_user_popup.open()

    def enter_UFO_coordinates(self):
        self.save_UFO_popup.open()

    def add_user_coordinates(self, lat, lon):
        self.add_user_marker(lat, lon)
        self.pathTracker.add_point((lat, lon))

    def add_UFO_coordinates(self, lat, lon):
        self.add_UFO_marker(lat, lon)
        self.pathTracker.add_point((lat, lon))

    def add_UFO_marker(self, lat, lon):
        if not self._layer_added:
            self.ids.map_view.add_layer(self._lineLayer, mode="scatter")
            self._layer_added = True
        marker = MapMarker(lat=lat, lon=lon, source='alien100.png', size=(1, 0.1), size_hint=(None, None),
                           allow_stretch=True)
        self.ids.map_view.add_marker(marker)

    def add_user_marker(self, lat, lon):
        marker = MapMarker(lat=lat, lon=lon, source='user_location.png', size=(1, 0.1), size_hint=(None, None),
                           allow_stretch=True)
        self.ids.map_view.add_marker(marker)
