from random import randint, random, sample, uniform
from math import ceil, floor, pi


class Genotype:
    _MUTATIONS_CHANCE = 1/5  # percentage of individuals that get changed
    _MUTATION_POINTS_AMOUNT = 3
    _AMOUNT_OF_CROSSOVER_POINTS = 1/5

    def __init__(self, vectors, wheel_vertices, wheel_proporties):
        self._vectors = vectors
        self._wheel_vertices = wheel_vertices
        self._wheel_properties = wheel_proporties  # radius, speed, friction, engineTorque
        self._fitness = float("inf")

    def evaluate_fitness(self, position):
        self._fitness = position
    
    def get_fitness(self):
        return self._fitness
    
    def _get_genes_from_parameters(self):
        genotype = []
        genotype.extend(self._vectors)
        genotype.extend(self._wheel_vertices)
        genotype.extend(self._wheel_properties)
        return genotype
    
    def _replace_parameters_from_genes(self, genes):
        vectors, wheel_vertices, wheel_properties = self._get_parameters_from_genes(genes)
        self._vectors = vectors
        self._wheel_vertices = wheel_vertices
        self._wheel_properties = wheel_properties
    
    def _get_parameters_from_genes(self, genes):
        vectors = genes[:len(self._vectors)]
        wheel_vertices = genes[len(self._vectors):len(self._vectors)+len(self._wheel_vertices)]
        wheel_properties = genes[len(self._vectors)+len(self._wheel_vertices):]
        return vectors, wheel_vertices, wheel_properties

    def _create_child_from_gene(self, genes):
        vectors, wheel_parameters, wheel_properties = self._get_parameters_from_genes(genes)
        return Genotype(vectors, wheel_parameters, wheel_properties)

    def create_pair_by_multipoints(self, other_parent):
        first_parent_genes = self._get_genes_from_parameters()
        second_parent_genes = self._get_genes_from_parameters()
        indexes = sorted(sample(range(0, len(first_parent_genes)-1), ceil(len(first_parent_genes)*self._AMOUNT_OF_CROSSOVER_POINTS)))
        first_child_genes = []
        second_child_genes = []
        indexes_index = 0
        switched = False
        for (index, first_parent_gene), second_parent_gene in zip(enumerate(first_parent_genes), second_parent_genes):
            if(switched):
                first_child_genes.append(second_parent_gene)
                second_child_genes.append(first_parent_gene)
            else:
                first_child_genes.append(first_parent_gene)
                second_child_genes.append(second_parent_gene)
            if(indexes_index < len(indexes) and index == indexes[indexes_index]):
                indexes_index += 1
                switched = not switched
        first_child = self._create_child_from_gene(first_child_genes)
        second_child = self._create_child_from_gene(second_child_genes)
        return first_child, second_child

    def mutate(self):
        if random() < self._MUTATIONS_CHANCE:  #while?
            amount_of_genes = len(self._vectors)+len(self._wheel_vertices)+len(self._wheel_properties)
            indexes = sample(range(amount_of_genes), self._MUTATION_POINTS_AMOUNT)
            for index in indexes:
                if index < len(self._vectors):
                    self._vectors[index] = (random() * 2 * pi, uniform(0.1, 4))
                elif index < len(self._vectors) + len(self._wheel_vertices):
                    index -= len(self._vectors)
                    self._wheel_vertices[index] = randint(0, 9)
                else:
                    index -= len(self._vectors) 
                    index -= len(self._wheel_vertices)
                    if index == 0:
                        self._wheel_properties[0] = (uniform(0.5, 2), uniform(0.5, 2))
                    elif index == 1:
                        self._wheel_properties[1] = (uniform(0, 100), uniform(0, 100))
                    elif index == 2:
                        self._wheel_properties[2] = (uniform(0, 1), uniform(0, 1))
                    else: 
                        self._wheel_properties[3] = (uniform(0, 100), uniform(0, 100))