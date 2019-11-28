import random
import numpy as np


def grasp_function_izaro_v2(numbers):
    s_data = sorted(numbers, reverse=True)
    half_indexes = random.sample(range(int(len(numbers) / 2)), int(len(numbers) / 2))
    pair_indexes = [(index * 2, index * 2 + 1) for index in half_indexes]
    a_mul = 1
    b_mul = 1
    chosen = np.zeros(len(numbers))
    for i in pair_indexes:
        index = 0 if a_mul < b_mul else 1
        num_ind_1 = numbers.index(s_data[i[index]])
        num_ind_2 = numbers.index(s_data[i[1 - index]])
        chosen[num_ind_1] = 1
        a_mul *= numbers[num_ind_1]
        b_mul *= numbers[num_ind_2]

    return list(map(int, list(chosen)))


def grasp_function_imanol(numbers, k=3):
    s_data = sorted(numbers, reverse=True)
    a_mul = 1
    b_mul = 1
    chosen = np.zeros(len(numbers))
    for i in range(int(len(numbers) / 2)):
        if k > len(s_data):
            k = len(s_data)

        sel_ind = random.sample(range(k), 2)
        sel_ind = sorted(sel_ind, reverse=True)

        num_ind_1 = numbers.index(s_data[sel_ind[0]])
        num_ind_2 = numbers.index(s_data[sel_ind[1]])

        del s_data[sel_ind[0]]
        del s_data[sel_ind[1]]

        group = 0 if a_mul < b_mul else 1
        max_ind = num_ind_2
        min_ind = num_ind_1
        if numbers[num_ind_1] > numbers[num_ind_2]:
            max_ind = num_ind_1
            min_ind = num_ind_2

        chosen[max_ind] = group
        chosen[min_ind] = 1 - group
        a_mul *= (numbers[max_ind] ** (1 - group) + numbers[min_ind] ** group)
        b_mul *= (numbers[max_ind] ** group + numbers[min_ind] ** (1 - group))

    return list(map(int, list(chosen)))


def get_initial_solution(numbers):
    initial = random.sample(range(len(numbers)), len(numbers))
    init_chosen = np.zeros(len(initial))
    init_chosen[initial[:int(len(initial) / 2)]] = 1
    return list(map(int, list(init_chosen)))
