import random
from .objective_function import *
import math


def get_best_neighbor(numbers, chosen, best, a, b):
    best_a = a
    best_b = b
    best_ = best
    best_chosen = chosen[:]
    one_indexes = [i for i, x in enumerate(chosen) if x == 1]
    zero_indexes = [i for i, x in enumerate(chosen) if x == 0]

    for zero_index in zero_indexes:
        for one_index in one_indexes:
            chosen_ = chosen[:]
            chosen_[zero_index] = 1
            chosen_[one_index] = 0
            value, var_a, var_b = objective_function_optim(a, b, numbers[one_index], numbers[zero_index])
            if value < best_:
                best_ = value
                best_chosen = chosen_[:]
                best_a = var_a
                best_b = var_b

    return best_chosen, best_, best_a, best_b


def get_neighbor_SA(numbers, chosen, best, a, b, iter_max=2, chain_max=30, c_k=35, w_ck=0.75):
    best_a = a
    best_b = b
    best_ = best
    best_chosen = chosen[:]
    one_indexes = [i for i, x in enumerate(chosen) if x == 1]
    zero_indexes = [i for i, x in enumerate(chosen) if x == 0]
    try:
        for num_iter in range(iter_max):
            for chain_size in range(chain_max):
                one_index = random.choice(one_indexes)
                zero_index = random.choice(zero_indexes)
                chosen_ = chosen[:]
                chosen_[zero_index] = 1
                chosen_[one_index] = 0
                value, var_a, var_b = objective_function_optim(a, b, numbers[one_index], numbers[zero_index])
                delta = value - best
                if delta < 0:
                    best_ = value
                    best_chosen = chosen_[:]
                    best_a = var_a
                    best_b = var_b

                    raise Exception("DELTA NEGATIVE")
                else:
                    aleat = random.random()
                    # log(delta) erabiltea planteau leike edo c_k handiagoak, diferentziek handiek izin ahal direlako
                    if 10*math.e ** (-5*math.log(delta) / c_k) > aleat:
                        best_ = value
                        best_chosen = chosen_[:]
                        best_a = var_a
                        best_b = var_b
                        raise Exception("WORSE SELECTED")
            c_k *= w_ck
    except Exception as e:
        pass
    return best_chosen, best_, best_a, best_b


def get_better_neighbor(numbers, chosen, best, a, b):
    best_a = a
    best_b = b
    best_ = best
    best_chosen = chosen[:]
    one_indexes = [i for i, x in enumerate(chosen) if x == 1]
    zero_indexes = [i for i, x in enumerate(chosen) if x == 0]
    try:
        for zero_index in zero_indexes:
            for one_index in one_indexes:
                chosen_ = chosen[:]
                chosen_[zero_index] = 1
                chosen_[one_index] = 0
                value, var_a, var_b = objective_function_optim(a, b, numbers[one_index], numbers[zero_index])
                if value < best_:
                    best_ = value
                    best_chosen = chosen_[:]
                    best_a = var_a
                    best_b = var_b
                    raise Exception
    except Exception:
        pass

    return best_chosen, best_, best_a, best_b
