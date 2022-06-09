import random
from math import sqrt

import numpy as np
from geopy import distance


class SignalEntry:
    def __init__(self, lat: float, lon: float, strength: float):
        self.lat = lat
        self.lon = lon
        self.strength = strength


class ProbabiltyCalculator:
    signal_multiplier = 1. / 1000
    rng = random.Random()

    def __init__(self):
        self.signals = []

    @staticmethod
    def manual_entry_to_probability(signal_entry: SignalEntry, lat: float, lon: float, ratio: float):
        dist = distance.geodesic((signal_entry.lat, signal_entry.lon), (lat, lon)).m
        most_probable_dist = (ratio / signal_entry.strength)

        ret = max((1. - abs(dist - most_probable_dist) / 4000, 0.))
        # if True or ret != 0:
        #     print('porbab:', ret, dist, most_probable_dist)

        return ret

    def add_signal(self, lat: float, lon: float, strength: float):
        self.signals.append(SignalEntry(lat, lon, strength * ProbabiltyCalculator.signal_multiplier))

    def get_probab_manual(self, lat: float, lon: float, ratio: float):
        # return 0.5

        sum = 0
        for signal_entry in self.signals:
            sum += ProbabiltyCalculator.manual_entry_to_probability(signal_entry, lat, lon, ratio)

        return 0 if len(self.signals) == 0 else sum / len(self.signals)

        # return min([ProbabiltyCalculator.rng.random() * ratio, 1])

    def get_best_ratio(self):
        accuracy = 20
        max_prob = 0
        max_ratio = 0

        for ratio in range(0, 200):
            current_max_prob = 0
            for signal_entry in self.signals:
                most_probable_dist = (ratio / signal_entry.strength)
                r = most_probable_dist/1000
                for i in range(0, accuracy):
                    angle = i * (2 * np.pi) / accuracy
                    x = r * np.cos(angle)
                    y = r * np.sin(angle)
                    r_earth = 6378
                    new_latitude = signal_entry.lat + (y / r_earth) * (180 / np.pi)
                    new_longitude = signal_entry.lon + (x / r_earth) * (180 / np.pi) / np.cos(
                        signal_entry.lat * np.pi / 180)

                    current_max_prob = max(current_max_prob, self.get_probab_manual(new_latitude, new_longitude, ratio))
            print(f"current ratio: {ratio}, max ratio {max_ratio}")
            print(f"current prob: {current_max_prob}, max prob {max_prob}")
            if (len(self.signals) > 2 and current_max_prob > max_prob) or current_max_prob > max_prob + 0.005:
                max_ratio = ratio
                max_prob = current_max_prob

        return max_ratio
