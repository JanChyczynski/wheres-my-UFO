from kivy.garden.mapview import MapView, MapMarker
from kivy.app import App
"""
to install 
pip install kivy
pip install mapview
pip install kivy-garden
garden install mapview
"""

class MapViewApp(App):
    def build(self):
        mapview = MapView(zoom=15, lat=50.049683, lon=19.944544)
        mapview.add_marker(MapMarker(lat=50, lon=20))
        return mapview


if __name__ == "__main__":
    MapViewApp().run()
