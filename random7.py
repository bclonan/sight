import colorsys
import random
import tkinter as tk

import pandas as pd

# Cell class to represent each cell in the grid


class Cell:
    def __init__(self, value, schema='default_schema', machine_set='default_set'):
        self.value = value
        self.schema = schema
        self.machine_set = machine_set
        self.color = self.calculate_color()

    # Calculate the color based on the value, schema, and machine set
    def calculate_color(self):
        hue = (self.value * 36) % 360
        if self.schema == 'schema1' and self.machine_set == 'set1':
            hue += 50
        elif self.schema == 'schema2' and self.machine_set == 'set2':
            hue += 100
        r, g, b = colorsys.hls_to_rgb(hue / 360, 0.5, 1)
        return f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'

# ResonanceGrid class to manage the grid


class ResonanceGrid:
    def __init__(self, matrix):
        self.grid = [[Cell(value) for value in row] for row in matrix]
        self.current_frequency = 1

    # Display the grid on a canvas
    def display(self, canvas):
        cell_size = 10
        for x, row in enumerate(self.grid):
            for y, cell in enumerate(row):
                canvas.create_rectangle(y * cell_size, x * cell_size,
                                        (y + 1) * cell_size, (x + 1) * cell_size,
                                        fill=cell.color, outline='')

    # Calculate the average color of the grid
    def average_color(self):
        total_r = total_g = total_b = 0
        total_cells = len(self.grid) * len(self.grid[0])
        for row in self.grid:
            for cell in row:
                r, g, b = int(cell.color[1:3], 16), int(
                    cell.color[3:5], 16), int(cell.color[5:7], 16)
                total_r += r
                total_g += g
                total_b += b
        avg_r = total_r / total_cells
        avg_g = total_g / total_cells
        avg_b = total_b / total_cells
        return f'#{int(avg_r):02x}{int(avg_g):02x}{int(avg_b):02x}'

    # Apply resonance effect to the grid
    def apply_resonance(self, frequency, root):
        self.current_frequency = frequency
        for row in self.grid:
            for cell in row:
                cell.value = (cell.value + frequency) % 10
                cell.color = cell.calculate_color()
        avg_color = self.average_color()
        root.title(f"Resonance Grid Simulation - Average Color: {avg_color}")

# Main function to set up the Tkinter window and grid


def main():
    root = tk.Tk()
    root.title("Resonance Grid Simulation")
    base_grid = pd.read_csv('a.csv', header=None).values.tolist()

    # Replace with your method of generating grid values
    resonance_grid = ResonanceGrid(base_grid)
    # Replace with your method of generating grid values
    grid_values = [[random.randint(0, 9)
                    for _ in range(100)] for _ in range(100)]
    resonance_grid = ResonanceGrid(grid_values)

    canvas = tk.Canvas(root, width=1000, height=1000)
    canvas.pack()

    # Redraw the grid
    def redraw():
        canvas.delete("all")
        resonance_grid.display(canvas)

    # Event handler for mouse clicks
    def on_click(event):
        frequency = random.randint(1, 9)
        resonance_grid.apply_resonance(frequency, root)
        redraw()

    canvas.bind("<Button-1>", on_click)
    redraw()
    root.mainloop()


if __name__ == "__main__":
    main()
