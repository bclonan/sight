import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw
import colorsys
import hashlib
import itertools
import math


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
            if x >= len(self.grid):
                break
            self.grid[x][y].value = int(bit)
            self.grid[x][y].color = self.grid[x][y].calculate_color()

    def encode_grid_to_bitstream(self):
        bits = ''
        for row in self.grid:
            for cell in row:
                bits += str(cell.value)
        return bits

    def save_grid_as_image(self, file_path):
        img_size = len(self.grid[0]) * 10, len(self.grid) * 10
        img = Image.new('RGB', img_size)
        draw = ImageDraw.Draw(img)
        for x, row in enumerate(self.grid):
            for y, cell in enumerate(row):
                draw.rectangle([y * 10, x * 10, y * 10 + 9,
                               x * 10 + 9], fill=cell.color)
        img.save(file_path)


def generate_pattern(grid_size):
    pattern = [int(math.fmod(math.fib(i), 10)) for i in range(grid_size**2)]
    return pattern


def generate_hash_from_grid(grid):
    grid_state = ''.join(cell.color for row in grid for cell in row)
    return hashlib.sha256(grid_state.encode()).hexdigest()


def main():
    root = tk.Tk()
    root.title("File to Grid Mapping")
    root.geometry("1200x1000")

    file_path = None

    def load_file():
        nonlocal file_path
        file_path = filedialog.askopenfilename()
        if file_path:
            grid_size = int(math.sqrt(os.path.getsize(file_path)))
            pattern = generate_pattern(grid_size)
            matrix = [[pattern[i * grid_size + j]
                       for j in range(grid_size)] for i in range(grid_size)]
            resonance_grid = ResonanceGrid(matrix)
            canvas.delete("all")
            resonance_grid.display(canvas)
            hash_value = generate_hash_from_grid(resonance_grid.grid)
            print(f"Hash: {hash_value}")
            proof_of_work(hash_value, resonance_grid)

    def proof_of_work(target_hash, grid):
        target_zeros = 75
        while not target_hash.startswith('0' * target_zeros):
            grid.map_bits_to_grid(grid.encode_grid_to_bitstream())
            target_hash = generate_hash_from_grid(grid.grid)
            print(f"Hash: {target_hash}")

    canvas = tk.Canvas(root, width=1000, height=1000)
    canvas.pack(side=tk.LEFT)

    load_button = tk.Button(root, text="Load File", command=load_file)
    load_button.pack(side=tk.RIGHT, padx=20)

    redraw()
    root.mainloop()


if __name__ == "__main__":
    main()
