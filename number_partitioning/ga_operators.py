from number_partitioning.solution_selectors import get_initial_solution, grasp_function_imanol, grasp_function_izaro_v2
from number_partitioning.objective_function import objective_function
from random import sample, random


def create_offsprings(parents, num_offspring):
    offsprings = []
    for _ in range(num_offspring):
        p = sample(parents, 2)
        offsprings.append(crossover(p[0], p[1]))

    return offsprings


def mutation_process(offsprings, mut_prob=.3):
    for i in range(len(offsprings)):
        prob = random()
        if prob > mut_prob:
            offsprings[i] = mutate(offsprings[i])

    return offsprings


def crossover(ind1, ind2, random_cuts=False):
    n = len(ind1)
    cut_indexes = [int(n * 1 / 3), int(n * 2 / 3)]
    if random_cuts:
        cut_indexes = sorted(sample(range(n), 2))
    offspring = ind1[:cut_indexes[0]] + ind2[cut_indexes[0]:cut_indexes[1]] + ind1[cut_indexes[1]:]
    index = 0
    if sum(offspring) > int(n / 2):
        index = 1
    return repair_offspring(offspring, index, n)


def repair_offspring(offspring, index, n):
    indexes = [i for i, x in enumerate(offspring) if x == index]
    extra_len = len(indexes) - int(n / 2)
    change_indexes = sample(indexes, extra_len)
    for i in change_indexes:
        offspring[i] = 1 - index
    return offspring


def mutate(ind):
    mut_ind = ind[:]
    change_index = sample(range(len(mut_ind)), 1)[0]
    indexes = [i for i, x in enumerate(mut_ind) if x == (1 - mut_ind[change_index])]
    mut_ind[change_index] = 1 - mut_ind[change_index]
    change_index = sample(indexes, 1)[0]
    mut_ind[change_index] = 1 - mut_ind[change_index]
    return mut_ind


def select(individuals, fitnesses, parent_num):
    sorted_fitnesses = sorted(enumerate(fitnesses), key=lambda x: x[1])
    best_indexes = list(zip(*sorted_fitnesses))[0][:parent_num]
    return [individuals[index] for index in best_indexes]


def evaluate(data, individuals):
    return [objective_function(data, ind)[0] for ind in individuals]


def genetic_algorithm(data, population=100, generations=100, parent_num=100, solution_generation=get_initial_solution):
    pop = [solution_generation(data) for _ in range(population)]
    for a in range(generations):
        fitnesses = evaluate(data, pop)
        parents = select(pop, fitnesses, parent_num)
        offsprings = create_offsprings(parents, population - parent_num)
        offsprings = mutation_process(offsprings)
        pop[:parent_num] = parents
        pop[parent_num:] = offsprings

    best_index = fitnesses.index(min(fitnesses))

    return pop[best_index], fitnesses[best_index]
