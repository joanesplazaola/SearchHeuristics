from collections import defaultdict

from number_partitioning.ga_operators import *
from number_partitioning.local_search import *
from number_partitioning.neighbor_selectors import *
import numpy as np
import time
import pandas as pd

instances = range(1, 11)
numbers = [50]
best_izaro = defaultdict(list)
best_imanol = defaultdict(list)
best_random = defaultdict(list)

multistart = 5

time_izaro = defaultdict(list)
time_imanol = defaultdict(list)
time_random = defaultdict(list)

for _ in range(20):
    for num in numbers:
        print(num)
        for instance in instances:
            with open(f"NumPart/Part{num}Instance{instance}") as file:
                data = list(map(int, file.readlines()))
                data = data[1:]

                start = time.time()
                izaro = local_search_multi(data, multistart, init_fn=grasp_function_izaro_v2)
                time_izaro[f"{num}_{instance}"].append(time.time() - start)

                start = time.time()
                imanol = local_search_multi(data, multistart, init_fn=grasp_function_imanol)
                time_imanol[f"{num}_{instance}"].append(time.time() - start)

                start = time.time()
                rand = local_search_multi(data, multistart, init_fn=get_initial_solution)
                time_random[f"{num}_{instance}"].append(time.time() - start)

                best_izaro[f"{num}_{instance}"].append(izaro)
                best_imanol[f"{num}_{instance}"].append(imanol)
                best_random[f"{num}_{instance}"].append(rand)

all_results = {"Pairs": best_izaro,
               "KMax": best_imanol,
               "Random": best_random
               }
result_dict = defaultdict(dict)

for name, values in all_results.items():
    for k, v in values.items():
        instance = k.split("_")[1]

        result_dict[k][f"{name}_avg"] = sum(v) / len(v)
        result_dict[k][f"{name}_std"] = format(np.std(v), '.3e')

df = pd.DataFrame(result_dict).T

all_results = {"Pairs": time_izaro,
               "KMax": time_imanol,
               "Random": time_random
               }
result_dict = defaultdict(dict)

for name, values in all_results.items():
    for k, v in values.items():
        instance = k.split("_")[1]
        result_dict[k][name] = f"{format((sum(v) / len(v)), '.3e')} ± {format(np.std(v), '.3e')}"

df_time = pd.DataFrame(result_dict).T

df_time.to_latex()
