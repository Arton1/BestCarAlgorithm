import random
import math


class Genotype:


    evaluation = float("inf")

    def __init__(self):
        self.vectors = []
        self.wheelVertices = []
        self.wheelProporties = []  # radius, speed, friction, engineTorque

        for i in range(0, 10): self.vectors.append((random.random() * 2 * math.pi, random.uniform(0.1, 4)))
        self.vectors.sort()
        self.wheelVertices.append(random.randint(0, 9))
        self.wheelVertices.append(random.randint(0, 9))
        self.wheelProporties.append((random.uniform(0.5, 2), random.uniform(0.5, 2)))
        self.wheelProporties.append((random.uniform(0, 100), random.uniform(0, 100)))
        self.wheelProporties.append((random.uniform(0, 1), random.uniform(0, 1)))
        self.wheelProporties.append((random.uniform(0, 100), random.uniform(0, 100)))

    def __repr__(self):
       return str(self.wheelVertices) + str(self.evaluation)
