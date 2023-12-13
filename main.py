import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageOps
import pandas as pd
import colorsys
import numpy as np
import os


class Cell:
    def __init__(self, value):
        self.value = value
        self.color = self.calculate_color()

    def calculate_color(self):
        hue = (self.value * 36) % 360
        r, g, b = colorsys.hls_to_rgb(hue / 360, 0.5, 1)
        return f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'


class ResonanceGrid:
    def __init__(self, matrix):
        self.grid = [[Cell(value) for value in row] for row in matrix]

    def display(self, canvas):
        cell_size = 10
        for x, row in enumerate(self.grid):
            for y, cell in enumerate(row):
                canvas.create_rectangle(y * cell_size, x * cell_size,
                                        (y + 1) * cell_size, (x + 1) * cell_size,
                                        fill=cell.color, outline='')

    def map_bits_to_grid(self, bitstream):
        for i, bit in enumerate(bitstream):
            x = i // len(self.grid[0])
            y = i % len(self.grid[0])
            if x < len(self.grid):
                self.grid[x][y].value = int(bit)
                self.grid[x][y].color = self.grid[x][y].calculate_color()

    def encode_grid_to_bitstream(self):
        bits = ''
        for row in self.grid:
            for cell in row:
                bits += str(cell.value)
        return bits

# Convert file to a bitstream


def file_to_bitstream(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
    return ''.join(f'{byte:08b}' for byte in content)

# Main function to set up the Tkinter window and grid


def main():
    root = tk.Tk()
    root.title("File to Grid Mapping")
    root.geometry("1200x1000")

    base_grid = pd.read_csv('a.csv', header=None).values.tolist()
    resonance_grid = ResonanceGrid(base_grid)

    canvas = tk.Canvas(root, width=1000, height=1000)
    canvas.pack(side=tk.LEFT)

    def redraw():
        canvas.delete("all")
        resonance_grid.display(canvas)

    def load_file():
        file_path = filedialog.askopenfilename()
        if file_path:
            bitstream = file_to_bitstream(file_path)
            resonance_grid.map_bits_to_grid(bitstream)
            redraw()

    load_button = tk.Button(root, text="Load File", command=load_file)
    load_button.pack(side=tk.RIGHT, padx=20)

    def save_bitstream():
        bitstream = resonance_grid.encode_grid_to_bitstream()
        with open("output_bitstream.txt", "w") as file:
            file.write(bitstream)
        print("Bitstream saved to output_bitstream.txt")

    save_button = tk.Button(root, text="Save Bitstream",
                            command=save_bitstream)
    save_button.pack(side=tk.RIGHT, padx=20)

    redraw()
    root.mainloop()


if __name__ == "__main__":
    main()
