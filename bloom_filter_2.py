import hashlib
import time
import sys
import math


class BloomFilter:


    def __init__(self, m, k):
        self.m = m
        self.k = k
        self.bits = [0] * m

    def _get_positions(self, element):
        positions = []

        for i in range(self.k):
            text = str(i) + ":" + str(element)
            digest = hashlib.sha256(text.encode()).hexdigest()
            number = int(digest, 16)
            position = number % self.m

            positions.append(position)

        return positions

    def add(self, element):
        positions = self._get_positions(element)
    
        for p in positions:
            self.bits[p] = 1

    def contains(self, element):
        positions = self._get_positions(element)

        for p in positions:
            if self.bits[p] == 0:
                return False

        return True





m = 100000
k = 7


brojevi_elemenata = [1000, 3000, 5000, 7000, 10000]


nedodani = [f"nepoznat_{i}" for i in range(5000)]


dodani = [f"element_{i}" for i in range(10000)]

print("EKSPERIMENT: UTJECAJ BROJA ELEMENATA")
print(f"Broj bitnih pozicija m = {m}")
print(f"Broj hash pozicija k = {k}")
print(f"Broj provjeravanih nedodanih elemenata = {len(nedodani)}")

print("\nREZULTATI")
print("-" * 75)
print(f"{'n':>8} | {'Lazno pozitivni':>16} | {'Empirijska stopa':>17} | {'Teorijska stopa':>16}")
print("-" * 75)

for n in brojevi_elemenata:

   
    bf = BloomFilter(m, k)

    
    for element in dodani[:n]:
        bf.add(element)

   
    lazno_pozitivni = 0

    for element in nedodani:
        if bf.contains(element):
            lazno_pozitivni += 1

    
    empirijska_stopa = lazno_pozitivni / len(nedodani)

   
    teorijska_stopa = (1 - math.exp(-k * n / m)) ** k

    print(
        f"{n:8} | "
        f"{lazno_pozitivni:16} | "
        f"{empirijska_stopa:16.4%} | "
        f"{teorijska_stopa:15.4%}"
    )

print("-" * 75)

