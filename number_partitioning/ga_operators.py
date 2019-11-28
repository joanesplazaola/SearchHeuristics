from number_partitioning.solution_selectors import *
from number_partitioning.objective_function import objective_function


def create_offsprings(parents, num_offspring):
    offsprings = []
    for _ in range(num_offspring):
        p = random.sample(parents, 2)
        offsprings.append(crossover(p[0], p[1]))

    return offsprings


def mutation_process(offsprings, mut_prob=.3):
    for i in range(len(offsprings)):
        prob = random.random()
        if prob > mut_prob:
            offsprings[i] = mutate(offsprings[i])

    return offsprings


def crossover(ind1, ind2):
    n = len(ind1)
    cut_indexes = sorted(random.sample(range(n), 2))
    offspring = ind1[:cut_indexes[0]] + ind2[cut_indexes[0]:cut_indexes[1]] + ind1[cut_indexes[1]:]
    index = 0
    if sum(offspring) > int(n / 2):
        index = 1
    return repair_offspring(offspring, index, n)


def repair_offspring(offspring, index, n):
    indexes = [i for i, x in enumerate(offspring) if x == index]
    extra_len = len(indexes) - int(n / 2)
    change_indexes = random.sample(indexes, extra_len)
    offspring = np.array(offspring)
    offspring[change_indexes] = 1 - index
    return list(offspring)


def mutate(ind):
    mut_ind = ind[:]
    change_index = random.sample(range(len(mut_ind)), 1)[0]
    indexes = [i for i, x in enumerate(mut_ind) if x == (1 - mut_ind[change_index])]
    mut_ind[change_index] = 1 - mut_ind[change_index]
    change_index = random.sample(indexes, 1)[0]
    mut_ind[change_index] = 1 - mut_ind[change_index]
    return mut_ind


def select(individuals, fitnesses, parent_num):
    ind = np.argpartition(fitnesses, parent_num)[:parent_num]

    return list(map(list, np.array(individuals)[ind]))


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

    best_index = np.argmin(fitnesses)

    return pop[best_index], fitnesses[best_index]
