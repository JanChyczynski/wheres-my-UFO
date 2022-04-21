from kivy.garden.mapview import MapView, MapMarkerPopup, MapMarker
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel

import localisationVisualizer
import signalFinder

"""
to install 
pip install kivy
pip install mapview
pip install kivy-garden
garden install mapview
"""


class MainLayout(TabbedPanel):
    pass


class MapViewApp(App):
    DEFAULT_LAT = 50.049683
    DEFAULT_LON = 19.944544

    def build(self):
        return MainLayout()


if __name__ == "__main__":
    MapViewApp().run()
