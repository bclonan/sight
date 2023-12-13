import pandas as pd
import random


class Cell:
    def __init__(self, value):
        self.value = value
        self.color = 'white'  # Initially colorless

    def spin_effect(self, neighbors):
        # Define the whirlwind effect here
        # For simplicity, let's say the value becomes the average of its neighbors
        self.value = sum(neighbors) / len(neighbors)

    def update_color(self):
        # Update the color based on the new value
        # Here we can define a new color mapping based on the value
        if self.value < 2:
            self.color = 'blue'
        elif self.value < 3:
            self.color = 'green'
        else:
            self.color = 'red'


class GameGrid:
    def __init__(self, matrix):
        self.grid = [[Cell(value) for value in row] for row in matrix]

    def display(self):
        for row in self.grid:
            print(' '.join(cell.color[0].upper() for cell in row))

    def spin_cells(self):
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                neighbors = self.get_neighbors_values(x, y)
                self.grid[x][y].spin_effect(neighbors)
        # After spinning, update colors
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                self.grid[x][y].update_color()

    def get_neighbors_values(self, x, y):
        # Get the values of neighboring cells
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(self.grid) and 0 <= ny < len(self.grid[0]) and (dx, dy) != (0, 0):
                    neighbors.append(self.grid[nx][ny].value)
        return neighbors


def main():
    # Initialize the game grid with a sample matrix
    base_grid = pd.read_csv('/a.csv', header=None).values.tolist()
    game_grid = GameGrid(base_grid)

    while True:
        game_grid.display()
        input("Press Enter to spin cells...")
        game_grid.spin_cells()


if __name__ == "__main__":
    main()
