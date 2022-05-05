from kivy.garden.mapview import MapView, MapMarkerPopup, MapMarker
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from saveDialog import SaveDialog

Builder.load_file('localisationVisualiser.kv')


class LocalisationVisualizer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.save_popup = SaveDialog(self)

    def add_coordinates(self):
        self.save_popup.open()

    def add_marker(self, lat, lon, size=1):
        print("asd", lat, lon)
        marker = MapMarkerPopup(lat=lat, lon=lon, source='alien100.png', popup_size=(100*size, 100*size), size_hint=(None, None),
                           allow_stretch=True)
        self.ids.map_view.center_on(lat, lon)
        self.ids.map_view.add_marker(marker)

