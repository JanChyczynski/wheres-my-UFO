from kivy.garden.mapview import MapView, MapMarkerPopup, MapMarker
from kivy.uix.boxlayout import BoxLayout

from saveDialog import SaveDialog


class SignalFinder(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.save_popup = SaveDialog(self)

    def add_coordinates(self):
        self.save_popup.open()

    def add_marker(self, lat, lon):
        print("asd", lat, lon)
        marker = MapMarker(lat=lat, lon=lon, source='alien100.png', size=(1, 0.1), size_hint=(None, None),
                           allow_stretch=True)
        self.ids.map_view.add_marker(marker)
