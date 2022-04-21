from kivy.garden.mapview import MapView, MapMarkerPopup, MapMarker
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel

"""
to install 
pip install kivy
pip install mapview
pip install kivy-garden
garden install mapview
"""


class SaveDialog(Popup):

    def __init__(self, parent_widget, **kwargs):  # my_widget is now the object where popup was called from.
        super(SaveDialog, self).__init__(**kwargs)

        self.parent_widget = parent_widget

    def save(self, *args):
        self.parent_widget.add_marker(lat=float(self.ids.lat_txt_in.text),
                                      lon=float(self.ids.lon_txt_in.text))
        self.dismiss()

    def cancel(self, *args):
        self.dismiss()


class LocalisationVisualizer(BoxLayout):
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


class MainLayout(TabbedPanel):
    pass


class MapViewApp(App):
    DEFAULT_LAT = 50.049683
    DEFAULT_LON = 19.944544

    def build(self):
        # box = LocalisationVisualizer()
        # mapview = MapView(
        # marker_popup = MapMarkerPopup(lat=50.050683, lon=19.954544, source='alien100.png')
        # App.get_running_app().root.ids.map_view.add_marker(marker_popup)
        # App.get_running_app().root.ids.map_view.add_marker(MapMarkerPopup(lat=50.051683, lon=19.934544))

        # box.add_widget(self.mapview)
        return MainLayout()


if __name__ == "__main__":
    MapViewApp().run()
