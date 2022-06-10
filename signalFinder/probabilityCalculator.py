import random

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

        return ret

    def add_signal(self, lat: float, lon: float, strength: float):
        self.signals.append(SignalEntry(lat, lon, strength * ProbabiltyCalculator.signal_multiplier))

    def get_probab_manual(self, lat: float, lon: float, ratio: float):
        probabs_sum = 0
        for signal_entry in self.signals:
            probabs_sum += ProbabiltyCalculator.manual_entry_to_probability(signal_entry, lat, lon, ratio)

        return 0 if len(self.signals) == 0 else probabs_sum / len(self.signals)

    def calculate_ratio(self, start=0, end=200, step=1):
        org_step = step
        accuracy = 20
        max_prob = 0
        max_ratio = 0

        ratio = start
        while ratio < end:
            current_max_prob = 0
            for signal_entry in self.signals:
                most_probable_dist = (ratio / signal_entry.strength)
                r = most_probable_dist / 1000
                for i in range(0, accuracy):
                    angle = i * (2 * np.pi) / accuracy
                    x = r * np.cos(angle)
                    y = r * np.sin(angle)
                    r_earth = 6378
                    new_latitude = signal_entry.lat + (y / r_earth) * (180 / np.pi)
                    new_longitude = signal_entry.lon + (x / r_earth) * (180 / np.pi) / np.cos(
                        signal_entry.lat * np.pi / 180)

                    current_max_prob = max(current_max_prob, self.get_probab_manual(new_latitude, new_longitude, ratio))
            # print(f"current ratio: {ratio}, max ratio {max_ratio}")
            # print(f"current prob: {current_max_prob}, max prob {max_prob}")
            if (len(self.signals) > 2 and current_max_prob > max_prob) or current_max_prob > max_prob + 0.005:
                max_ratio = ratio
                max_prob = current_max_prob
            if current_max_prob > max(0.6, 1 - (len(self.signals)) * 0.8):
                step = max(1, org_step // 3)
            else:
                step = org_step

            ratio += step

        return max_ratio

    def get_best_ratio(self):
        max_ratio = self.calculate_ratio(0, 200, 10)
        return self.calculate_ratio(max(0, max_ratio - 10), min(200, max_ratio + 10), 1)
