import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageOps
import pandas as pd
import random
import colorsys
import numpy as np

# Cell class represents each cell in the grid


class Cell:
    def __init__(self, value):
        self.value = value
        self.color = self.calculate_color()

    # Calculate color based on the cell's value
    def calculate_color(self):
        hue = (self.value * 36) % 360
        r, g, b = colorsys.hls_to_rgb(hue / 360, 0.5, 1)
        return f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'

# ResonanceGrid class manages the grid and image mapping


class ResonanceGrid:
    def __init__(self, matrix):
        self.grid = [[Cell(value) for value in row] for row in matrix]

    # Display the grid on the canvas
    def display(self, canvas):
        cell_size = 10
        for x, row in enumerate(self.grid):
            for y, cell in enumerate(row):
                canvas.create_rectangle(y * cell_size, x * cell_size,
                                        (y + 1) * cell_size, (x + 1) * cell_size,
                                        fill=cell.color, outline='')

    # Map an image to the grid based on color similarity
    def map_image_to_grid(self, image):
        img_resized = ImageOps.fit(
            image, (len(self.grid[0]), len(self.grid)), Image.LANCZOS)
        img_data = np.array(img_resized)

        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                closest_match = self.find_closest_match(img_data[y, x])
                self.grid[y][x].value = closest_match
                self.grid[y][x].color = self.grid[y][x].calculate_color()

    # Find the closest matching grid value for a given pixel
    def find_closest_match(self, pixel):
        min_diff = float('inf')
        match_value = 0
        for i in range(10):  # Grid values range from 0 to 9
            r, g, b = colorsys.hls_to_rgb(i * 36 / 360, 0.5, 1)
            diff = sum(abs(val - comp)
                       for val, comp in zip(pixel[:3], (r, g, b)))
            if diff < min_diff:
                min_diff = diff
                match_value = i
        return match_value

# Main function to set up the Tkinter window and grid


def main():
    root = tk.Tk()
    root.title("Image to Grid Mapping")
    root.geometry("1200x1000")

    # Load grid from CSV
    base_grid = pd.read_csv('a.csv', header=None).values.tolist()
    resonance_grid = ResonanceGrid(base_grid)

    canvas = tk.Canvas(root, width=1000, height=1000)
    canvas.pack(side=tk.LEFT)

    # Redraw the grid on the canvas
    def redraw():
        canvas.delete("all")
        resonance_grid.display(canvas)

    # Load and map an image to the grid
    def load_image():
        file_path = filedialog.askopenfilename()
        if file_path:
            img = Image.open(file_path)
            resonance_grid.map_image_to_grid(img)
            redraw()

    load_button = tk.Button(root, text="Load Image", command=load_image)
    load_button.pack(side=tk.RIGHT, padx=20)

    redraw()
    root.mainloop()


if __name__ == "__main__":
    main()
