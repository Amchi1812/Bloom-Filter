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



n = 10000
k = 7

# Testiramo razlicite velicine Bloomovog filtera
velicine_filtera = [20000, 50000, 100000, 200000]

# Elementi koje dodajemo i elementi koje ne dodajemo
dodani = [f"element_{i}" for i in range(n)]
nedodani = [f"nepoznat_{i}" for i in range(5000)]

print("EKSPERIMENT: UTJECAJ VELICINE FILTERA")
print(f"Broj dodanih elemenata n = {n}")
print(f"Broj hash pozicija k = {k}")
print(f"Broj provjeravanih nedodanih elemenata = {len(nedodani)}")

print("\nREZULTATI")
print("-" * 95)
print(
    f"{'m':>8} | {'Lazno pozitivni':>16} | "
    f"{'Empirijska stopa':>17} | {'Teorijska stopa':>16} | "
    f"{'Memorija (KiB)':>15}"
)
print("-" * 95)

for m in velicine_filtera:

    # Kreiramo novi filter za svaku vrijednost m
    bf = BloomFilter(m, k)

    # Dodajemo istih 10.000 elemenata
    for element in dodani:
        bf.add(element)

    # Provjeravamo nedodane elemente
    lazno_pozitivni = 0

    for element in nedodani:
        if bf.contains(element):
            lazno_pozitivni += 1

    # Izracun empirijske stope
    empirijska_stopa = lazno_pozitivni / len(nedodani)

    # Izracun teorijske stope
    teorijska_stopa = (1 - math.exp(-k * n / m)) ** k

    # Procjena memorije liste bitova i razlicitih vrijednosti 0 i 1
    memoria_bloom = sys.getsizeof(bf.bits)

    for vrijednost in set(bf.bits):
        memoria_bloom += sys.getsizeof(vrijednost)

    print(
        f"{m:8} | "
        f"{lazno_pozitivni:16} | "
        f"{empirijska_stopa:16.4%} | "
        f"{teorijska_stopa:15.4%} | "
        f"{memoria_bloom / 1024:15.2f}"
    )

print("-" * 95)