def calculate_average(models):
    if len(models) == 0:
        return 0

    total = 0

    for model in models:
        total += model["score"]

    return total / len(models)

