"""Charts simulation data.

Even if there is only one infected person, it is still possible that more than 3/4 of population gets infected.

I ended up getting the whole population to become infected on the first try which is a sign that people should not
party during COVID. :)
"""
import argparse
from projects.pj02.model import Model
from typing import List


def main() -> None:
    """Entrypoint of program."""
    parser = argparse.ArgumentParser(description='Charts infection and immunization curves for simulation.')
    parser.add_argument('cells', type=int, help='How many cells')
    parser.add_argument('speed', type=float, help='Speed of the cell')
    parser.add_argument('infected', type=int, help='Initial number of infected cells')
    parser.add_argument('immune', type=int, help='Initial number of immune cells')
    args = parser.parse_args()

    model = Model(args.cells, args.speed, args.infected, args.immune)
    num_infected: List[int] = [args.infected]
    num_immune: List[int] = [args.immune]
    time_ticks: List[int] = [0]

    while not model.is_complete():
        model.tick()
        time_ticks.append(model.time)
        current_infected: int = 0
        current_immune: int = 0
        for cell in model.population:
            if cell.is_infected():
                current_infected += 1
            if cell.is_immune():
                current_immune += 1
        num_infected.append(current_infected)
        num_immune.append(current_immune)

    chart(time_ticks, num_infected, num_immune)


def chart(ticks: List[int], infected: List[int], immune: List[int]) -> None:
    """Charts the data."""
    import matplotlib.pyplot as plt
    plt.plot(ticks, infected)
    plt.plot(ticks, immune)
    plt.title("Infection and Immunization Curves of a Simulation")
    plt.xlabel("Time Ticks in Simulation")
    plt.ylabel("Number of Cells")
    plt.show()


if __name__ == "__main__":
    main()