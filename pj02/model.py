"""The model classes maintain the state and logic of the simulation."""

from __future__ import annotations
from typing import List
from random import random
from projects.pj02 import constants
from math import sin, cos, pi, sqrt


__author__ = "730395239"


class Point:
    """A model of a 2-d cartesian coordinate Point."""
    x: float
    y: float

    def __init__(self, x: float, y: float):
        """Construct a point with x, y coordinates."""
        self.x = x
        self.y = y

    def add(self, other: Point) -> Point:
        """Add two Point objects together and return a new Point."""
        x: float = self.x + other.x
        y: float = self.y + other.y
        return Point(x, y)

    def distance(self, other: Point) -> float:
        """Finds distance between two points."""
        dist: float = sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)
        return dist


class Cell:
    """An individual subject in the simulation."""
    location: Point
    direction: Point
    sickness: int = constants.VULNERABLE

    def __init__(self, location: Point, direction: Point):
        """Construct a cell with its location and direction."""
        self.location = location
        self.direction = direction

    def tick(self) -> None:
        """Changes location and monitors infected period."""
        self.location = self.location.add(self.direction)
        if self.is_infected():
            self.sickness += 1
        if self.sickness > constants.RECOVERY_PERIOD:
            self.sickness = -1
        
    def color(self) -> str:
        """Changes color of cell depending on status."""
        if self.is_vulnerable():
            return "gray"
        if self.is_immune():
            return "blue"
        else:
            return "red"
    
    def contract_disease(self) -> None:
        """Assigns sickness to infected status."""
        self.sickness = constants.INFECTED

    def is_vulnerable(self) -> bool:
        """Tests if cell is vulnerable."""
        if self.sickness == constants.VULNERABLE:
            return True
        else:
            return False

    def is_infected(self) -> bool:
        """Tests if cell is infected."""
        if self.sickness >= constants.INFECTED:
            return True
        else:
            return False

    def contact_with(self, other: Cell) -> None:
        """Changes state of cell when made contact with another."""
        if self.is_infected() and other.is_vulnerable():
            other.contract_disease()
        if self.is_vulnerable() and other.is_infected():
            self.contract_disease()

    def immunize(self) -> None:
        """Assigns sickness to immune status."""
        self.sickness = constants.IMMUNE

    def is_immune(self) -> bool:
        """Tests if cell is immune."""
        if self.sickness == constants.IMMUNE:
            return True
        else:
            return False


class Model:
    """The state of the simulation."""

    population: List[Cell]
    time: int = 0

    def __init__(self, cells: int, speed: float, initial_infected: int, immune: int = 0):
        """Initialize the cells with random locations and directions."""
        if initial_infected <= 0 or initial_infected >= cells:
            raise ValueError("Some number of cells must begin infected.")
        if immune < 0 or immune >= cells:
            raise ValueError("Initial immune cells cannot be negative or equal/exceed total cells.")
        self.population = []
        for i in range(0, initial_infected):
            start_loc = self.random_location()
            start_dir = self.random_direction(speed)
            new_cell: Cell = Cell(start_loc, start_dir)
            new_cell.sickness = constants.INFECTED
            self.population.append(new_cell)
        for i in range(0, immune):
            start_loc = self.random_location()
            start_dir = self.random_direction(speed)
            new_cell = Cell(start_loc, start_dir)
            new_cell.sickness = constants.IMMUNE
            self.population.append(new_cell)
        for i in range(0, cells - immune - initial_infected):
            start_loc = self.random_location()
            start_dir = self.random_direction(speed)
            new_cell = Cell(start_loc, start_dir)
            self.population.append(new_cell)
        
    def tick(self) -> None:
        """Update the state of the simulation by one time step."""
        self.time += 1
        for cell in self.population:
            cell.tick()
            self.enforce_bounds(cell)
        self.check_contacts()

    def random_location(self) -> Point:
        """Generate a random location."""
        start_x = random() * constants.BOUNDS_WIDTH - constants.MAX_X
        start_y = random() * constants.BOUNDS_HEIGHT - constants.MAX_Y
        return Point(start_x, start_y)

    def random_direction(self, speed: float) -> Point:
        """Generate a 'point' used as a directional vector."""
        random_angle = 2.0 * pi * random()
        dir_x = cos(random_angle) * speed
        dir_y = sin(random_angle) * speed
        return Point(dir_x, dir_y)

    def enforce_bounds(self, cell: Cell) -> None:
        """Cause a cell to 'bounce' if it goes out of bounds."""
        if cell.location.x > constants.MAX_X:
            cell.location.x = constants.MAX_X
            cell.direction.x *= -1
        if cell.location.x < constants.MIN_X:
            cell.location.x = constants.MIN_X
            cell.direction.x *= -1
        if cell.location.y > constants.MAX_Y:
            cell.location.y = constants.MAX_Y
            cell.direction.y *= -1
        if cell.location.y < constants.MIN_Y:
            cell.location.y = constants.MIN_Y
            cell.direction.y *= -1

    def is_complete(self) -> bool:
        """Method to indicate when the simulation is complete.""" 
        for a_cell in self.population:
            if a_cell.is_infected():
                return False
        return True

    def check_contacts(self) -> None:
        """Tests whether any two cells have come in contact."""
        for i in range(0, len(self.population)):
            for j in range(i + 1, len(self.population)):
                if self.population[i].location.distance(self.population[j].location) < constants.CELL_RADIUS:
                    self.population[i].contact_with(self.population[j])
