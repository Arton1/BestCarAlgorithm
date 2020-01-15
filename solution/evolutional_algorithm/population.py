from solution.evolutional_algorithm.genotype import Genotype
from random import randint, random, uniform, sample
from math import ceil, pi


class Population:
    vertices = 4
    _AMOUNT_OF_CANDIDATES = 10
    _AMOUNT_OF_CHILDREN = _AMOUNT_OF_CANDIDATES
    _TOURNAMENT_SIZE = 2

    def __init__(self,
                 candidates_amount=_AMOUNT_OF_CANDIDATES,
                 children_amount=_AMOUNT_OF_CHILDREN,
                 ):
        self._candidates = []
        self._generation = 1
        self._children_amount = children_amount
        self._tournament_size = self._TOURNAMENT_SIZE
        self._create_starting_population(candidates_amount)

    def _create_starting_population(self, candidates_amount):
        for candidate in range(candidates_amount):
            # vectors = [(random() * 2 * pi, uniform(0.1, 4)) for vector in range(self.vertices)]
            intervals = [0]
            for i in range(0, self.vertices):
                intervals.append(intervals[-1] + 360 / self.vertices)
            vectors = []
            for i in range(0, self.vertices):
                vectors.append((uniform(intervals[i], intervals[i + 1]) * 3.14 / 180, uniform(0.1, 4)))

            # vectors.sort()
            wheel_vertices = []
            wheel_vertices.append(randint(0, self.vertices - 1))
            wheel_vertices.append(randint(0, self.vertices - 1))
            wheel_properties = []
            wheel_properties.append((uniform(0.5, 2), uniform(0.5, 2)))
            wheel_properties.append((uniform(10, 40), uniform(10, 40)))
            wheel_properties.append((uniform(0, 1), uniform(0, 1)))
            wheel_properties.append((uniform(200, 200), uniform(200, 200)))
            individual = Genotype(vectors, wheel_vertices, wheel_properties)
            self._candidates.append(individual)

    def print_information(self):
        sum = 0
        print(f"Generacja: {self._generation}")
        for index, genotype in enumerate(sorted(self._candidates, key=lambda x: x.get_fitness(), reverse=True)):
            fitness = genotype.get_fitness()
            print(f"{index + 1} : {fitness}")
            sum += fitness
        return sum, self._generation
        # print(f"{index+1}: {individual.get_information()} : {fitness}")

    def set_fitness(self, world):
        for (genotype, i) in zip(self._candidates, range(2, 3 * len(self._candidates) + 2, 3)):
            genotype.evaluate_fitness(world.bodies[i].position[0])

    def _set_best(self):
        best_fitness = self._best_genotype.get_fitness()
        for genotype in self._candidates:
            genotype_fitness = genotype.get_fitness()
            if best_fitness > genotype.get_fitness():
                best = genotype
                best_fitness = genotype_fitness
        self._best_genotype = best

    def _roulette_select_individual(self, candidates):
        fitness_sum = sum(candidate.get_fitness() for candidate in candidates)
        spin = random()
        probability_sum = 0
        for potential_parent in candidates:
            fitness = potential_parent.get_fitness()
            probability = fitness / fitness_sum
            probability_sum += probability
            if probability_sum > spin:
                return potential_parent

    def _tournament_select_individual(self, candidates):
        tournament_candidates = sample(candidates, self._tournament_size)
        return min(tournament_candidates, key=lambda x: x.get_fitness())

    def _ranking_select_individual(self, candidates):
        candidates.sort(key=lambda x: x.get_fitness())
        rank_sum = (len(candidates) + 1) * len(candidates) / 2
        spin = randint(0, rank_sum)
        index_sum = 0
        for index, candidate in enumerate(candidates, start=1):
            if spin <= index_sum + index:
                return candidate
            index_sum += index

    def _best_select_individual(self, candidates_with_fitness):
        return max(candidates, key=lambda x: x.get_fitness())

    def _select_pair_of_parents(self):
        first_parent = self._tournament_select_individual(self._candidates)
        self._candidates.remove(first_parent)
        second_parent = self._tournament_select_individual(self._candidates)
        self._candidates.append(first_parent)
        return first_parent, second_parent

    def _create_children(self):
        children = []
        for pair_of_parents in range(0, self._children_amount, 2):
            first_parent, second_parent = self._select_pair_of_parents()
            pair_of_children = Genotype.create_pair_by_multipoints(first_parent, second_parent)
            for child in pair_of_children:
                child.mutate()
                children.append(child)
        return children

    def _update_population(self, children):
        self._candidates = children

    def evolve(self, amount_of_iterations=1):
        for i in range(amount_of_iterations):
            children = self._create_children()
            self._update_population(children)
            self._generation += 1
