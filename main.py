"""Main file to run the program."""

from labb2 import get_pokemon_data, print_test_data_predictions


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


if __name__ == "__main__":
    main()
