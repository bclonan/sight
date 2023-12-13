import tkinter as tk
import pandas as pd
import random


class Cell:
    def __init__(self, value, x, y):
        self.value = value
        self.x = x
        self.y = y
        self.color = self.calculate_color()

    def calculate_color(self):
        # Custom color based on position and value
        red = (self.value * 123 + self.x * 45) % 256
        green = (self.value * 156 + self.y * 67) % 256
        blue = (self.value * 189 + (self.x + self.y) * 89) % 256
        return f'#{int(red):02x}{int(green):02x}{int(blue):02x}'

    def update_value_based_on_spiral(self, spiral_power):
        self.value = (self.value + spiral_power) % 360
        self.color = self.calculate_color()


class GameGrid:
    def __init__(self, matrix):
        self.grid = [[Cell(value, x, y) for y, value in enumerate(row)]
                     for x, row in enumerate(matrix)]

    def apply_spiral_effect(self, x_center, y_center, spiral_power):
        for x, row in enumerate(self.grid):
            for y, cell in enumerate(row):
                distance = ((x - x_center) ** 2 + (y - y_center) ** 2) ** 0.5
                if distance <= spiral_power:
                    cell.update_value_based_on_spiral(spiral_power)

    def display(self, canvas):
        cell_size = 10  # Size of each cell in pixels
        for x, row in enumerate(self.grid):
            for y, cell in enumerate(row):
                canvas.create_rectangle(y * cell_size, x * cell_size,
                                        (y + 1) * cell_size, (x + 1) * cell_size,
                                        fill=cell.color, outline='')


def main():
    root = tk.Tk()
    root.title("Game Grid")

    base_grid = pd.read_csv('a.csv', header=None).values.tolist()
    game_grid = GameGrid(base_grid)

    canvas = tk.Canvas(root, width=1000, height=1000)
    canvas.pack()

    def redraw():
        canvas.delete("all")
        game_grid.display(canvas)

    def on_click(event):
        x, y = event.x // 10, event.y // 10
        spiral_power = 5
        game_grid.apply_spiral_effect(x, y, spiral_power)
        redraw()

    canvas.bind("<Button-1>", on_click)
    redraw()
    root.mainloop()


if __name__ == "__main__":
    main()
