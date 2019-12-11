import random
import math


class Genotype:
    vectors = []
    wheelVertices = []
    wheelProporites = []  # radius, speed, fraction

    evaluation = float("inf")

    def newRandom(self):
        for i in range(0, 10): self.vectors.append((random.random() * 2 * math.pi, random.uniform(0.1, 4)))
        self.wheelVertices.append(random.randint(0, 10))
        self.wheelVertices.append(random.randint(0, 10))
        self.wheelProporites.append(random.uniform(0.5, 2))
        self.wheelProporites.append(random.uniform(0, 100))
        self.wheelProporites.append(random.uniform(0, 1))

    def printGene(self):
        print(self.vectors)