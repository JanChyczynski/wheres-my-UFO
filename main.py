from kivy.app import App
from kivy.lang import Builder
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


Builder.load_file('mainLayout.kv')


class MapViewApp(App):
    DEFAULT_LAT = 50.049683
    DEFAULT_LON = 19.944544
    DEFAULT_IP = "127.0.0.1"
    DEFAULT_PORT = 55672
    DEFAULT_SAMPLE_RATE = 3.2e6
    DEFAULT_CENTER_FREQ = 95e6
    DEFAULT_GAIN = 5

    def build(self):
        return MainLayout()


if __name__ == "__main__":
    import os

    cwd = os.getcwd()
    MapViewApp().run()
