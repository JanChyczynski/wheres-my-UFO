from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel

import locationVisualizer
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
    DEFAULT_IP = "127.0.0.1"
    DEFAULT_PORT = 55672

    def build(self):
        return MainLayout()


if __name__ == "__main__":
    MapViewApp().run()
