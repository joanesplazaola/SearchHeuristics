def objective_function_optim(a, b, num_a, num_b):
    new_a = int(a / num_a) * num_b
    new_b = int(b / num_b) * num_a
    return abs(new_a - new_b), new_a, new_b


def objective_function(data, chosen):
    a1 = 1
    b1 = 1
    for a in range(len(data)):
        a1 *= data[a] ** chosen[a]
        b1 *= data[a] ** (1 - chosen[a])
    return abs(a1 - b1), a1, b1
