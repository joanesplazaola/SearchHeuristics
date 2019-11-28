from .objective_function import objective_function
from number_partitioning.neighbor_selectors import get_best_neighbor
from number_partitioning.solution_selectors import *

def local_search(numbers, chosen, best, a, b):
    while True:
        local_best_chosen, local_best, a, b = get_best_neighbor(numbers, chosen, best, a, b)
        if local_best_chosen == chosen:
            break
        chosen = local_best_chosen[:]
        best = local_best
    return chosen, best


def local_search_multi(numbers, multistart=5, init_fn=grasp_function_izaro_v2, **kwargs):
    chosen = init_fn(numbers, **kwargs)
    best, a, b = objective_function(numbers, chosen)
    chosen_list = []
    best_list = []
    for _ in range(multistart):
        chosen, best = local_search(numbers, chosen, best, a, b)
        chosen_list.append(chosen)
        best_list.append(best)

        # We get a initial solution for the multistart
        chosen = init_fn(numbers, **kwargs)
        best, a, b = objective_function(numbers, chosen)

    index_min = np.argmin(best_list)

    return best_list[index_min]
