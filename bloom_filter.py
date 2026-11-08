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


dodani = [f"element_{i}" for i in range(n)]


nedodani = [f"nepoznat_{i}" for i in range(n)]


bf = BloomFilter(100000, 7)
obican_skup = set()


pocetak = time.perf_counter()


for element in dodani:
    bf.add(element)

vrijeme_bloom_dodavanje = time.perf_counter() - pocetak


pocetak = time.perf_counter()

for element in dodani:
    obican_skup.add(element)

vrijeme_set_dodavanje = time.perf_counter() - pocetak


pocetak = time.perf_counter()

for element in dodani:
    bf.contains(element)

vrijeme_bloom_provjera = time.perf_counter() - pocetak


pocetak = time.perf_counter()

for element in dodani:
    element in obican_skup

vrijeme_set_provjera = time.perf_counter() - pocetak

memoria_bloom = sys.getsizeof(bf.bits)
for vrijednost in set(bf.bits):
    memoria_bloom += sys.getsizeof(vrijednost)


memoria_set = sys.getsizeof(obican_skup)
for e in obican_skup:
    memoria_set += sys.getsizeof(e)


print("BROJ ELEMENATA:", n)

print("\nVRIJEME DODAVANJA")

print(f"Bloom filter: {vrijeme_bloom_dodavanje * 1000:.2f} ms")
print(f"set:          {vrijeme_set_dodavanje * 1000:.2f} ms")

print("\nVRIJEME PROVJERE")
print(f"Bloom filter: {vrijeme_bloom_provjera * 1000:.2f} ms")
print(f"set:          {vrijeme_set_provjera * 1000:.2f} ms")


print("\nPROCJENA MEMORIJE")
print(f"Bloomov filter: {memoria_bloom} bajtova")
print(f"Python set: {memoria_set} bajtova")

print("\nPROCJENA MEMORIJE U KB")
print(f"Bloomov filter: {memoria_bloom / 1024:.2f} KB")
print(f"Python set: {memoria_set /1024:.2f} KB")


if memoria_bloom < memoria_set:
    usteda = (1 - memoria_bloom / memoria_set) * 100
    print(f"\nProcijenjena usteda memorije: {usteda:.2f}%")
else:
    dodatno = (memoria_bloom / memoria_set - 1) * 100
    print(f"\nBloom filter koristi približno {dodatno:.2f}% više memorije.")
