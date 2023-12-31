"""
Pokemon module used for importing pokemons from a file,
as well as functions for measurments and predictions of pokemons.
"""


import statistics
from dataclasses import dataclass
from math import sqrt
import random


@dataclass(slots=True, frozen=True)
class Pokemon:
    """Lightweight Pokemon dataclass"""

    width: float
    height: float
    # None type is used when you predict type, based on width and height
    pokemon_type: int | None = None


def get_pokemon_data() -> tuple[list[Pokemon], list[Pokemon]]:
    """Read pokemon data from file and return lists based on types."""
    pichus = []
    pikachus = []
    # Load training data
    with open("datapoints.txt", "r", encoding="utf-8") as data_file:
        # First line is header info.
        # (width (cm), height (cm), label (0-pichu, 1-pikachu))
        # Just discard the first line.
        data_file.readline()

        # The rest of the lines are pokemon data.
        for line in data_file.read().splitlines():
            values = line.split(", ")

            width = float(values[0])
            height = float(values[1])
            pokemon_type = int(values[2])

            pokemon = Pokemon(width, height, pokemon_type)

            if pokemon_type == 1:
                pikachus.append(pokemon)
            else:
                pichus.append(pokemon)

    return pikachus, pichus


def print_test_data_predictions(all_pokemons: list[Pokemon]) -> None:
    """Get pokemons from testdata file."""
    with open("testpoints.txt", "r", encoding="utf-8") as testpoints_file:
        # First line is header info.
        # Test points:
        # Just discard the first line.
        testpoints_file.readline()
        # The rest of the lines are pokemon data.
        for line in testpoints_file.read().splitlines():
            # First value is line number,
            # so we just disregard it.
            start = line.index("(") + 1
            stop = -1
            pokemon_values = line[start:stop].split(", ")
            width, height = map(float, pokemon_values)
            pokemon = Pokemon(width, height)
            predition = predict_pokemon_type(all_pokemons, pokemon)
            pokemon_type_string = "Pikachu" if predition == 1 else "Pichu"
            print(
                f"Sample with (width, height): ({width}, {height}) "
                + f"classified as {pokemon_type_string}"
            )


def print_predicted_type_from_user_input(
    pokemons: list[Pokemon],
    n_closest: int = 1,
) -> None:
    "Predict type of pokemon based on values input by the user."
    measurement = get_pokemon_from_input()
    prediction = predict_pokemon_type(pokemons, measurement, n_closest)
    prediction_string = "Pikachu" if prediction else "Pichu"
    closest_string = "den" if n_closest == 1 else f"dom {n_closest}"
    print(
        f"(bredd, längd): ({measurement.width}, "
        + f"{measurement.height}) klassificeras som "
        + f"{prediction_string} (baserat på jämförelse med {closest_string} närmaste.)"
    )


def get_pokemon_from_input() -> Pokemon:
    """Read input from keyboard until user has typed every value correct."""

    width = read_failsafe_input("bredd")
    height = read_failsafe_input("längd")

    return Pokemon(width, height)


def read_failsafe_input(measurement_string: str) -> float:
    """Read input from keyboard until user inputs a valid value."""

    while True:
        value_input = input(
            f"Ange {measurement_string} i form av ett heltal eller decimaltal: "
        ).strip()

        try:
            value = float(value_input)
        except ValueError:
            print(f"{value_input} är inte kompatibelt med float. Försök igen.")

        if value < 0:
            print("Värdet måste vara större än eller lika med 0")
            continue
        break

    return value


def predict_pokemon_type(
    pokemon_list: list[Pokemon],
    measurement: Pokemon,
    n_closest: int = 1,
) -> int | None:
    """Predict pokemon type based on the n closest pokemons."""
    pokemon_type_list = [
        p.pokemon_type
        for p in get_n_closest_pokemons(pokemon_list, measurement, n_closest)
    ]

    # mode returns the most common values
    return statistics.mode(pokemon_type_list)


def get_n_closest_pokemons(
    pokemon_list: list[Pokemon],
    measurement: Pokemon,
    n_closest: int,
) -> list[Pokemon]:
    """Get the n closest pokemons to the measurement values"""
    return sorted(
        pokemon_list, key=lambda pokemon: pokemon_dinstance(pokemon, measurement)
    )[:n_closest]


def pokemon_dinstance(
    pokemon: Pokemon,
    measurement: Pokemon,
) -> float:
    """Get the "distance" between pokemon and a measurement based on width and height."""
    return sqrt(
        (pokemon.width - measurement.width) ** 2
        + (pokemon.height - measurement.height) ** 2
    )


def print_accuracy_stats(
    pikachus: list[Pokemon],
    pichus: list[Pokemon],
    iterations: int = 10,
) -> None:
    """Print accuracy a number of times based on \
    predictions on randomized training and test data."""
    # VG-assignment
    accuracies = []
    for iteration in range(iterations):
        print(f"Iteration: {iteration + 1}")
        training_data, test_data = prepare_randomized_training_and_test_data(
            pikachus, pichus
        )

        # Predict pokemons
        predictions = predict_pokemon_types(
            training_data,
            test_data,
        )

        # Filter out the types only
        actual_types = [pk.pokemon_type for pk in test_data]

        print("Förutsägelse   ", predictions)
        print("Faktiska typer ", actual_types)

        # Count the cases where prediction and actual value are the same
        right_answers = sum(
            1
            for prediction, actual in zip(predictions, actual_types)
            if prediction == actual
        )

        # Note: Only check accuracy against the test data
        number_of_pokemons = len(test_data)

        print(f"Rätta svar: {right_answers}")
        print(f"Antal pokemon: {number_of_pokemons}")

        accuracy = right_answers / number_of_pokemons
        accuracies.append(accuracy)

        print(f"Träffsäkerhet: {accuracy:.2%}")
        print()

    avg_accuracy = statistics.mean(accuracies)

    print(
        f"Genomsnittet för träffsäkerhet på {iterations} iterationer"
        + f" med {number_of_pokemons} slumpmässigt"
        + f" valda pokemons per iteration blev: {avg_accuracy:.2%}"
    )


def predict_pokemon_types(
    pokemons: list[Pokemon],
    measurements: list[Pokemon],
    n_closest: int = 1,
) -> list[int | None]:
    """Predict type based on measurement data."""
    # Should result in: Pikachu, Pikachu, Pikachu, Pichu

    pokemon_types = []
    for measurement in measurements:
        prediction = predict_pokemon_type(pokemons, measurement, n_closest)
        pokemon_types.append(prediction)
    return pokemon_types


def prepare_randomized_training_and_test_data(
    pikachus: list[Pokemon],
    pichus: list[Pokemon],
    training_amount: int = 50,
    test_amount: int = 25,
) -> tuple[list[Pokemon], list[Pokemon]]:
    """Prepare pokemon data for randomized predictions."""
    # Randomize lists
    random.shuffle(pikachus)
    random.shuffle(pichus)

    # Note: training_amount and test_amount are per
    # pokemon type (50 + 25 for pikachu and same for pichu)

    # Pick random samples
    training_pikachus = pikachus[:training_amount]
    test_pikachus = pikachus[training_amount : training_amount + test_amount]

    training_pichus = pichus[:training_amount]
    test_pichus = pichus[training_amount : training_amount + test_amount]

    # Reshuffle the training data
    training_data = training_pikachus + training_pichus
    random.shuffle(training_data)

    # Reshuffle the test data
    test_data = test_pikachus + test_pichus
    random.shuffle(test_data)

    # 100 samples of training_data, 50 samples of test_data
    return training_data, test_data
