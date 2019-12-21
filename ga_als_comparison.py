from collections import defaultdict

from number_partitioning.ga_operators import *
from number_partitioning.local_search import *
from number_partitioning.neighbor_selectors import *
import numpy as np
import time
import pandas as pd
deterministic = [269114681010, 118479464640, 202764848496, 1234214659656, 16768974600, 107714458776, 2041905009816,
                 10048311000, 60287671392, 12743488653]
instances = range(1, 11)
numbers = [10]
best_sa = defaultdict(list)
best_ga = defaultdict(list)

time_sa = defaultdict(list)
time_ga = defaultdict(list)

for _ in range(20):
    for num in numbers:
        print(num)
        for instance in instances:
            with open(f"NumPart/Part{num}Instance{instance}") as file:
                data = list(map(int, file.readlines()))
                data = data[1:]

                start = time.time()
                sa_ = local_search_multi(data, 5, neighbor_fn=get_neighbor_SA, )
                time_sa[f"{num}_{instance}"].append(time.time() - start)

                start = time.time()
                ga_ = genetic_algorithm(data, len(data) * 15, 30, int(len(data) / 4))[1]
                time_ga[f"{num}_{instance}"].append(time.time() - start)
                best_sa[f"{num}_{instance}"].append(sa_)
                best_ga[f"{num}_{instance}"].append(ga_)

all_results = {"SimmulatedAnnealing": best_sa,
               "GeneticAlgorithm": best_ga
               }
result_dict = defaultdict(dict)

for name, values in all_results.items():
    for k, v in values.items():
        instance = k.split("_")[1]
        result_dict[k]["Deterministic"] =  deterministic[int(instance) - 1]

        result_dict[k][f"{name}_avg"] = format(deterministic[int(instance) - 1] / (sum(v) / len(v)), '.3f')
        result_dict[k][f"{name}_std"] = format(np.std(v), '.3e')


df = pd.DataFrame(result_dict).T


all_results = {"SimmulatedAnnealing":time_sa,
               "GeneticAlgorithm": time_ga
               }
result_dict = defaultdict(dict)

for name, values in all_results.items():
    for k, v in values.items():
        instance = k.split("_")[1]
        result_dict[k][name] = f"{format((sum(v) / len(v)), '.3e')} ± {format(np.std(v), '.3e') }"

df_time = pd.DataFrame(result_dict).T


df_time.to_latex()
