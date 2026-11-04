
from calculator import calculate_average
models=[
    {"name": "GPT", "score": 80},
    {"name": "Claude", "score": 100}]
def test_calculate_average():
    assert calculate_average(models)==90

def test_calculate_average_empty():
    models = []

    result = calculate_average(models)

    assert result == 0
def test_average_single():
    models = [
        {"name": "GPT", "score": 95}
    ]

    result = calculate_average(models)

    assert result == 95
def test_decimal_average():
    models = [
        {"name": "GPT", "score": 80},
        {"name": "Claude", "score": 81},
    ]

    assert calculate_average(models) == 80.5