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






# Parametri koji ostaju isti
n = 10000
m = 100000

# Broj hash pozicija koji cemo testirati
vrijednosti_k = [1, 3, 5, 7, 9, 11, 13]

# Elementi za testiranje
dodani = [f"element_{i}" for i in range(n)]
nedodani = [f"nepoznat_{i}" for i in range(5000)]

print("EKSPERIMENT: UTJECAJ BROJA HASH POZICIJA")
print(f"Broj dodanih elemenata n = {n}")
print(f"Broj bitnih pozicija m = {m}")
print(f"Broj provjeravanih nedodanih elemenata = {len(nedodani)}")

print("\nREZULTATI")
print("-" * 105)
print(
    f"{'k':>4} | {'Lazno pozitivni':>16} | "
    f"{'Empirijska stopa':>17} | {'Teorijska stopa':>16} | "
    f"{'Vrijeme dodavanja (ms)':>22} | {'Vrijeme provjere (ms)':>21}"
)
print("-" * 105)

for k in vrijednosti_k:

    # Kreiramo novi filter za svaku vrijednost k
    bf = BloomFilter(m, k)

    # Mjerimo vrijeme dodavanja elemenata
    pocetak = time.perf_counter()

    for element in dodani:
        bf.add(element)

    vrijeme_dodavanja = (time.perf_counter() - pocetak) * 1000

    # Mjerimo vrijeme provjere nedodanih elemenata
    lazno_pozitivni = 0
    pocetak = time.perf_counter()

    for element in nedodani:
        if bf.contains(element):
            lazno_pozitivni += 1

    vrijeme_provjere = (time.perf_counter() - pocetak) * 1000

    # Izracun empirijske i teorijske stope
    empirijska_stopa = lazno_pozitivni / len(nedodani)
    teorijska_stopa = (1 - math.exp(-k * n / m)) ** k

    print(
        f"{k:4} | "
        f"{lazno_pozitivni:16} | "
        f"{empirijska_stopa:16.4%} | "
        f"{teorijska_stopa:15.4%} | "
        f"{vrijeme_dodavanja:22.2f} | "
        f"{vrijeme_provjere:21.2f}"
    )

print("-" * 105)

# Teorijski optimalan broj hash pozicija
k_opt = (m / n) * math.log(2)

print(f"\nTeorijski optimalan broj hash pozicija: {k_opt:.2f}")
