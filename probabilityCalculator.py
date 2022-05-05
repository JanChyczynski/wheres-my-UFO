import random


class SignalEntry:
    def __init__(self, lat:float, lon:float, strength:float):
        self.lat = lat
        self.lon = lon
        self.strength = strength


class ProbabiltyCalculator:
    rng = random.Random()

    def __init__(self):
        self.signals = []

    # def add_signal(self, signal_entry: SignalEntry):
    def add_signal(self, lat:float, lon:float, strength:float):
        self.signals.append(SignalEntry(lat, lon, strength))

    def get_probab_manual(self, lat:float, lon:float, ratio:float):
        return ProbabiltyCalculator.rng.random()
