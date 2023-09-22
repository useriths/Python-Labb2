"""Plotting pokemons."""
import matplotlib.pyplot as plt

from labb2 import Pokemon


def plot_all_pokemons(
    pikachus: list[Pokemon],
    pichus: list[Pokemon],
) -> None:
    """Plot pokemon measurements."""

    pikachu_widths = [p.width for p in pikachus]
    pikachu_heights = [p.height for p in pikachus]

    pichus_widths = [p.width for p in pichus]
    pichus_heights = [p.height for p in pichus]

    plt.title("Pokemon")

    plt.xlabel("bredd", color="blue")
    plt.ylabel("längd", color="blue", rotation=0)

    plt.scatter(
        pikachu_widths,
        pikachu_heights,
        marker="o",
        label="Pikachus",
        color="red",
    )
    plt.scatter(
        pichus_widths,
        pichus_heights,
        marker="x",
        label="Pichus",
        color="green",
    )

    plt.legend(loc="upper left")
    plt.show()
