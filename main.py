from number_partitioning.ga_operators import *
instances = range(1, 11)
numbers = [50]

for _ in range(10):
    for num in numbers:
        print(num)
        for instance in instances:
            with open(f"NumPart/Part{num}Instance{instance}") as file:
                data = list(map(int, file.readlines()))
                data = data[1:]

                print(genetic_algorithm(data, len(data) * 5, 50, int(len(data) / 2), ))
