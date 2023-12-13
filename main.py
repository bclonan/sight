import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw
import colorsys
import os
import hashlib


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


def file_to_grid(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
    grid_size = int(len(content)**0.5)
    matrix = [[int(content[i * grid_size + j])
               for j in range(grid_size)] for i in range(grid_size)]
    return matrix


def grid_to_file(matrix, file_path):
    grid_size = len(matrix)
    content = ''.join(str(matrix[i][j])
                      for i in range(grid_size) for j in range(grid_size))
    with open(file_path, 'wb') as file:
        file.write(content.encode())


def generate_hash_from_grid(grid):
    grid_state = ''.join(cell.color for row in grid for cell in row)
    return hashlib.sha256(grid_state.encode()).hexdigest()


def load_image(file_path):
    img = Image.open(file_path)
    width, height = img.size
    matrix = [[0 for _ in range(width)] for _ in range(height)]
    for x in range(width):
        for y in range(height):
            r, g, b = img.getpixel((x, y))
            gray_value = int((r + g + b) / 3)  # Convert to grayscale
            matrix[y][x] = 1 if gray_value > 128 else 0
    return matrix


def main():
    root = tk.Tk()
    root.title("File to Grid Mapping")
    root.geometry("1200x1000")

    base_grid = file_to_grid('a.csv')
    resonance_grid = ResonanceGrid(base_grid)

    canvas = tk.Canvas(root, width=1000, height=1000)
    canvas.pack(side=tk.LEFT)

    def redraw():
        canvas.delete("all")
        resonance_grid.display(canvas)

    file_path = None

    def load_file():
        nonlocal file_path
        file_path = filedialog.askopenfilename()
        if file_path:
            grid = file_to_grid(file_path)
            resonance_grid = ResonanceGrid(grid)
            redraw()
            hash_value = generate_hash_from_grid(resonance_grid.grid)
            print(f"Hash: {hash_value}")

    load_button = tk.Button(root, text="Load File", command=load_file)
    load_button.pack(side=tk.RIGHT, padx=20)

    def save_grid():
        nonlocal file_path
        if file_path:
            grid_to_file(resonance_grid.grid, file_path)
            print("Grid saved to:", file_path)

    save_button = tk.Button(root, text="Save Grid to File", command=save_grid)
    save_button.pack(side=tk.RIGHT, padx=20)

    def save_bitstream():
        nonlocal file_path
        if file_path:
            bitstream = resonance_grid.encode_grid_to_bitstream()
            save_path = filedialog.asksaveasfilename(
                defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if save_path:
                with open(save_path, "w") as file:
                    file.write(bitstream)
                print("Bitstream saved to:", save_path)

    save_bitstream_button = tk.Button(
        root, text="Save Bitstream", command=save_bitstream)
    save_bitstream_button.pack(side=tk.RIGHT, padx=20)

    def save_grid_image():
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            resonance_grid.save_grid_as_image(save_path)
            print("Grid image saved to:", save_path)

    save_image_button = tk.Button(
        root, text="Save Grid as Image", command=save_grid_image)
    save_image_button.pack(side=tk.RIGHT, padx=20)

    def load_from_image():
        nonlocal file_path, resonance_grid
        file_path = filedialog.askopenfilename()
        if file_path:
            matrix = load_image(file_path)
            resonance_grid = ResonanceGrid(matrix)
            redraw()

    load_from_image_button = tk.Button(
        root, text="Load From Image", command=load_from_image)
    load_from_image_button.pack(side=tk.RIGHT, padx=20)

    def load_bitstream():
        nonlocal file_path, resonance_grid
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                bitstream = file.read()
            grid_size = int(len(bitstream)**0.5)
            matrix = [[int(bitstream[i * grid_size + j])
                       for j in range(grid_size)] for i in range(grid_size)]
            resonance_grid = ResonanceGrid(matrix)
            redraw()

    load_bitstream_button = tk.Button(
        root, text="Load Bitstream", command=load_bitstream)
    load_bitstream_button.pack(side=tk.RIGHT, padx=20)

    redraw()
    root.mainloop()


if __name__ == "__main__":
    main()
