from collections import defaultdict

from number_partitioning.ga_operators import *
from number_partitioning.local_search import *
from number_partitioning.neighbor_selectors import *

instances = range(1, 11)
numbers = [10]
best_better = defaultdict(int)
best_best = defaultdict(int)
best_sa = defaultdict(int)
best_ga = defaultdict(int)

for _ in range(20):
    for num in numbers:
        print(num)
        for instance in instances:
            with open(f"NumPart/Part{num}Instance{instance}") as file:
                data = list(map(int, file.readlines()))
                data = data[1:]
                best_ = local_search_multi(data, 50, neighbor_fn=get_best_neighbor)
                better_ = local_search_multi(data, 50, neighbor_fn=get_better_neighbor)
                sa_ = local_search_multi(data, 50, neighbor_fn=get_neighbor_SA, )
                ga_ = genetic_algorithm(data, len(data)*15, 30, int(len(data)/4))[1]
                best = min([best_, better_, sa_, ga_])

                best_better[f"{num}_{instance}"] += (best_ == best)
                best_best[f"{num}_{instance}"] += (better_ == best)
                best_sa[f"{num}_{instance}"] += (sa_ == best)
                best_ga[f"{num}_{instance}"] += (ga_ == best)

import pandas as pd

pd.DataFrame([best_sa, best_better, best_best, best_ga], index=["Simulated annealing", "Better", "Best", "Genetic"]).T
