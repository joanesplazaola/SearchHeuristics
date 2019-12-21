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
best_better = defaultdict(list)
best_best = defaultdict(list)
best_sa = defaultdict(list)

time_better = defaultdict(list)
time_best = defaultdict(list)
time_sa = defaultdict(list)

for _ in range(20):
    for num in numbers:
        print(num)
        for instance in instances:
            with open(f"NumPart/Part{num}Instance{instance}") as file:
                data = list(map(int, file.readlines()))
                data = data[1:]

                start = time.time()
                best_ = local_search_multi(data, 50, neighbor_fn=get_best_neighbor)
                time_best[f"{num}_{instance}"].append(time.time() - start)

                start = time.time()
                better_ = local_search_multi(data, 50, neighbor_fn=get_better_neighbor)
                time_better[f"{num}_{instance}"].append(time.time() - start)

                start = time.time()
                sa_ = local_search_multi(data, 50, neighbor_fn=get_neighbor_SA, )
                time_sa[f"{num}_{instance}"].append(time.time() - start)

                best_better[f"{num}_{instance}"].append(better_)
                best_best[f"{num}_{instance}"].append(best_)
                best_sa[f"{num}_{instance}"].append(sa_)

all_results = {"Better": best_better,
               "Best": best_best,
               "SimmulatedAnnealing": best_sa,
               }
result_dict = defaultdict(dict)

for name, values in all_results.items():
    for k, v in values.items():
        instance = k.split("_")[1]
        result_dict[k]["Deterministic"] = deterministic[int(instance) - 1]

        result_dict[k][f"{name}_avg"] = format(deterministic[int(instance) - 1] / (sum(v) / len(v)), '.3f')
        result_dict[k][f"{name}_std"] = format(np.std(v), '.3e')

df = pd.DataFrame(result_dict).T

all_results = {"Better": time_better,
               "Best": time_best,
               "SimmulatedAnnealing": time_sa,
               }
result_dict = defaultdict(dict)

for name, values in all_results.items():
    for k, v in values.items():
        instance = k.split("_")[1]
        result_dict[k][name] = f"{format((sum(v) / len(v)), '.3e')} ± {format(np.std(v), '.3e')}"

df_time = pd.DataFrame(result_dict).T

df_time.to_latex()
