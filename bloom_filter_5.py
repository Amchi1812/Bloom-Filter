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






# Broj elemenata koji se dodaju u svaki filter
n = 10000

# Broj nedodanih elemenata za testiranje
broj_testova = 5000

dodani = [f"element_{i}" for i in range(n)]
nedodani = [f"nepoznat_{i}" for i in range(broj_testova)]

# Konfiguracije koje cemo uporediti: (m, k)
konfiguracije = [
    (20000, 3),
    (50000, 3),
    (50000, 4),
    (100000, 5),
    (100000, 7),
    (200000, 7),
    (200000, 14)
]

print("ZAVRSNI EKSPERIMENT BLOOMOVOG FILTERA")
print(f"Broj dodanih elemenata: {n}")
print(f"Broj testiranih nedodanih elemenata: {broj_testova}")

rezultati = []

for m, k in konfiguracije:

    # Kreiramo novi filter
    bf = BloomFilter(m, k)

    # Mjerenje vremena dodavanja
    pocetak = time.perf_counter()

    for element in dodani:
        bf.add(element)

    vrijeme_dodavanja = (time.perf_counter() - pocetak) * 1000

    # Mjerenje vremena provjere nedodanih elemenata
    lazno_pozitivni = 0
    pocetak = time.perf_counter()

    for element in nedodani:
        if bf.contains(element):
            lazno_pozitivni += 1

    vrijeme_provjere = (time.perf_counter() - pocetak) * 1000

    # Empirijska i teorijska stopa
    empirijska_stopa = lazno_pozitivni / broj_testova
    teorijska_stopa = (1 - math.exp(-k * n / m)) ** k

    # Procjena memorije trenutne Python implementacije
    memorija = sys.getsizeof(bf.bits)

    for vrijednost in set(bf.bits):
        memorija += sys.getsizeof(vrijednost)

    # Procenat bitnih pozicija postavljenih na 1
    jedinice = sum(bf.bits)
    popunjenost = jedinice / m * 100

    rezultati.append({
        "m": m,
        "k": k,
        "lazno_pozitivni": lazno_pozitivni,
        "empirijska": empirijska_stopa * 100,
        "teorijska": teorijska_stopa * 100,
        "dodavanje": vrijeme_dodavanja,
        "provjera": vrijeme_provjere,
        "memorija": memorija / 1024,
        "popunjenost": popunjenost
    })

# Ispis rezultata
print("\nREZULTATI")
print("-" * 125)

print(
    f"{'m':>8} | {'k':>3} | {'FP broj':>8} | "
    f"{'Emp. FP %':>10} | {'Teor. FP %':>11} | "
    f"{'Dod. ms':>9} | {'Prov. ms':>9} | "
    f"{'Mem. KiB':>10} | {'Popunjenost %':>14}"
)

print("-" * 125)

for r in rezultati:
    print(
        f"{r['m']:8} | "
        f"{r['k']:3} | "
        f"{r['lazno_pozitivni']:8} | "
        f"{r['empirijska']:10.4f} | "
        f"{r['teorijska']:11.4f} | "
        f"{r['dodavanje']:9.2f} | "
        f"{r['provjera']:9.2f} | "
        f"{r['memorija']:10.2f} | "
        f"{r['popunjenost']:14.2f}"
    )

print("-" * 125)

# Teorijski optimalan k za svaku konfiguraciju
print("\nTEORIJSKI OPTIMALAN BROJ HASH POZICIJA")

for m in sorted(set(r["m"] for r in rezultati)):
    k_opt = (m / n) * math.log(2)
    print(f"m = {m:6}: optimalni k ≈ {k_opt:.2f}")

