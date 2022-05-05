from kivy.garden.mapview import MapView, MapMarkerPopup, MapMarker
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from lineLayer import LineLayer
from pathTracker import PathTracker
from saveDialog import SaveDialog, SaveUserDialog

Builder.load_file('localisationVisualiser.kv')


class LocalisationVisualizer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.save_UFO_popup = SaveDialog(self)
        self.save_user_popup = SaveUserDialog(self)
        self._lineLayer = LineLayer(coordinates=[[0, 0], [0, 0]])
        self._layer_added = False
        self.pathTracker = PathTracker(self._lineLayer)

    def add_user_coordinates(self):
        self.save_user_popup.open()

    def add_UFO_coordinates(self):
        self.save_UFO_popup.open()

    def add_UFO_marker(self, lat, lon):
        print("heeej")
        if not self._layer_added:
            self.ids.map_view.add_layer(self._lineLayer, mode="scatter")
            self._layer_added = True
        self.pathTracker.add_point((lat, lon))
        marker = MapMarker(lat=lat, lon=lon, source='alien100.png', size=(1, 0.1), size_hint=(None, None),
                           allow_stretch=True)
        self.ids.map_view.add_marker(marker)

    def add_user_marker(self, lat, lon):
        self.pathTracker.add_point((lat, lon))
        marker = MapMarker(lat=lat, lon=lon, source='user_location.png', size=(1, 0.1), size_hint=(None, None),
                           allow_stretch=True)
        self.ids.map_view.add_marker(marker)
