import random
from math import sqrt

from geopy import distance


class SignalEntry:
    def __init__(self, lat: float, lon: float, strength: float):
        self.lat = lat
        self.lon = lon
        self.strength = strength


class ProbabiltyCalculator:
    signal_multiplier = 1./1000
    rng = random.Random()

    def __init__(self):
        self.signals = []

    @staticmethod
    def manual_entry_to_probability(signal_entry: SignalEntry, lat: float, lon: float, ratio: float):
        dist = distance.geodesic((signal_entry.lat, signal_entry.lon), (lat, lon)).m
        most_probable_dist = (ratio/signal_entry.strength)

        ret = max((1.-abs(dist-most_probable_dist)/4000, 0.))
        # if True or ret != 0:
        #     print('porbab:', ret, dist, most_probable_dist)

        return ret


    # def add_signal(self, signal_entry: SignalEntry):
    def add_signal(self, lat: float, lon: float, strength: float):
        self.signals.append(SignalEntry(lat, lon, strength*ProbabiltyCalculator.signal_multiplier))

    def get_probab_manual(self, lat: float, lon: float, ratio: float):
        # return 0.5

        sum = 0
        for signal_entry in self.signals:
            sum += ProbabiltyCalculator.manual_entry_to_probability(signal_entry, lat, lon, ratio)

        return 0 if len(self.signals) == 0 else sum/len(self.signals)

        # return min([ProbabiltyCalculator.rng.random() * ratio, 1])
