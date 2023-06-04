import random

class Person:
    population = 0

    def __init__(self, lantai, tinggi_lantai):
        self.animasi = None
        self.id = Person.population
        Person.population += 1
        self.lantai_awal = 0
        self.lantai_target = random.randint(1, lantai-1)
        while self.lantai_awal == self.lantai_target:
            self.lantai_target = random.randint(0, lantai-1)
        self.arah = (1 if self.lantai_awal < self.lantai_target else -1)
        self.jarak = tinggi_lantai * (self.lantai_awal - self.lantai_target)
        self.selesai = False
        self.dalam_lift = False
        self.wait_time = 0
        self.lift_spot = False

    def tiba(self, lantai):
        return True if lantai == self.lantai_target else False
    
    def menunggu(self):
        return not self.dalam_lift and not self.selesai