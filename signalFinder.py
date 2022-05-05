from kivy.garden.mapview import MapView, MapMarkerPopup, MapMarker
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from SignalMarker import SignalMarker
from saveDialog import SaveDialog, SignalSaveDialog
from main import MapViewApp

Builder.load_file('signalFinder.kv')

class MyMapMarker(MapMarker):
    pass

class SignalFinder(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.save_popup = SignalSaveDialog(self)
        self.signal_markers = []

    def add_coordinates(self):
        self.save_popup.open()

    def add_marker(self, lat, lon, strength=1):
        self.signal_markers.append(SignalMarker(lat, lon, strength, self.ids.map_view))
        self.ids.map_view.center_on(lat, lon)

    def update_markers(self, ratio):
        for marker in self.signal_markers:
            marker.update_signal_marker(ratio)

    # def slider_val_changed(self, value):
    #     self.update_markers(value)

