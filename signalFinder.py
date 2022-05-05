from kivy.garden.mapview import MapView, MapMarkerPopup, MapMarker
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from saveDialog import SaveSignalDialog

Builder.load_file('signalFinder.kv')


class SignalFinder(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.save_popup = SaveSignalDialog(self)

    def enter_coordinates(self):
        self.save_popup.open()

    def add_coordinates(self, lat, lon):
        self.add_marker(lat, lon)
        # TODO add to container

    def add_marker(self, lat, lon):
        print("asd", lat, lon)
        marker = MapMarker(lat=lat, lon=lon, source='alien100.png', size=(1, 0.1), size_hint=(None, None),
                           allow_stretch=True)
        self.ids.map_view.add_marker(marker)
