import threading

from kivy.clock import Clock
from kivy.garden.mapview import MapView, MapMarkerPopup, MapMarker
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from saveDialog import SaveSignalDialog
from probabilityCalculator import ProbabiltyCalculator
from heatmapLayer import HeatmapLayer

Builder.load_file('signalFinder.kv')


class SignalFinder(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.save_popup = SaveSignalDialog(self)
        self.probability_calculator = ProbabiltyCalculator()
        self.heatmap_layer = HeatmapLayer(self.probability_calculator)
        Clock.schedule_once(self.init_ui, 0)

    def init_ui(self, dt=0):
        self.ids.map_view.add_layer(self.heatmap_layer, mode='scatter')

    def calculate_ratio(self, dt=0):
        prev = self.ids.slider.value
        self.ids.slider.value = self.probability_calculator.get_best_ratio()
        if prev != self.ids.slider.value:
            self.heatmap_layer.reposition()

    def threaded_calculate_ratio(self):
        # Clock.schedule_once(self.calculate_ratio, 0)
        thread = RatioCalculateThread(self)
        thread.start()

    def enter_coordinates(self):
        self.save_popup.open()

    def add_coordinates(self, lat, lon, strength):
        self.add_marker(lat, lon)
        self.probability_calculator.add_signal(lat, lon, strength)
        self.heatmap_layer.reposition()

    def add_marker(self, lat, lon):
        print("asd", lat, lon)
        marker = MapMarker(lat=lat, lon=lon, source='resources/alien100.png', size=(1, 0.1), size_hint=(None, None),
                           allow_stretch=True)
        self.ids.map_view.add_marker(marker)


class RatioCalculateThread(threading.Thread):
    def __init__(self, signal_finder: SignalFinder):
        super().__init__()
        self.signal_finder = signal_finder

    def run(self) -> None:
        self.signal_finder.calculate_ratio()
