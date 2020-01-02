from random import randint, random, sample
from math import ceil, floor


class Genotype:
    _MUTATIONS_CHANCE = 1/5  # percentage of individuals that get changed
    _MUTATION_POINTS_AMOUNT = 1/30
    _AMOUNT_OF_CROSSOVER_POINTS = 1/5

    def __init__(self, vectors, wheel_verices, wheel_proporties):
        self._vectors = []
        self._wheel_vertices = []
        self._wheel_proporties = []  # radius, speed, friction, engineTorque
        self._fitness = float("inf")
        self._solution = []
        self._solution.extend(vectors, wheel_vertices, wheel_proporties)

    def evaluate_fitness(self, position):
        self._fitness = position
    
    def get_fitness(self):
        return self._fitness

    def create_pair_by_multipoints(self, other_individual):
        indexes = sorted(sample(range(0, len(self._solution)-1), ceil(len(self._solution)*self._AMOUNT_OF_CROSSOVER_POINTS)))
        first_child_solution = []
        second_child_solution = []
        indexes_index = 0
        switched = False
        for (index, first_parent_gene), second_parent_gene in zip(enumerate(self._solution), other_individual._solution):
            if(switched):
                first_child_solution.append(second_parent_gene)
                second_child_solution.append(first_parent_gene)
            else:
                first_child_solution.append(first_parent_gene)
                second_child_solution.append(second_parent_gene)
            if(indexes_index < len(indexes) and index == indexes[indexes_index]):
                indexes_index += 1
                switched = not switched
        return Individual(first_child_solution), Individual(second_child_solution)

    def mutate(self, min_score, max_score):
        while random() < self._MUTATIONS_CHANCE:
            for mutation in range(ceil(len(self._solution)*self._MUTATION_POINTS_AMOUNT)):
                self._solution[randint(0, len(self._solution)-1)] = randint(min_score, max_score)
