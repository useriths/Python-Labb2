"""Main file to run the program."""

from labb2 import (
    get_pokemon_data,
    print_accuracy_stats,
    print_predicted_type_from_user_input,
    print_test_data_predictions,
)
from plotting import plot_all_pokemons


def main() -> None:
    """Main function"""

    # Initialize values
    pikachus, pichus = get_pokemon_data()
    all_pokemons = pikachus + pichus

    # Assignments

    print("LABB 2")
    print()
    print("Klassificering av testdata från uppgiften:")
    print_test_data_predictions(all_pokemons)
    print()
    print(
        "Facit för uppgiften:\n"
        + "Sample with (width, height): (25, 32) classified as Pikachu\n"
        + "Sample with (width, height): (24.2, 31.5) classified as Pikachu\n"
        + "Sample with (width, height): (22, 34) classified as Pikachu\n"
        + "Sample with (width, height): (20.5, 34) classified as Pichu\n"
    )

    print("Uppgift 1")
    print_predicted_type_from_user_input(all_pokemons, 1)
    print()

    print("Uppgift 2")
    print_predicted_type_from_user_input(all_pokemons, 10)
    print()

    print("Uppgift 3 (VG)")
    print_accuracy_stats(pikachus, pichus)
    print()

    # Plot Pokemons
    plot_all_pokemons(pikachus, pichus)


if __name__ == "__main__":
    main()
