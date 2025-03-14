import tkinter as tk
import random
import colorsys
import pandas as pd
from PIL import Image, ImageDraw


class Cell:
    def __init__(self, value, schema='default_schema', machine_set='default_set', visibility=True, opacity=1.0):
        self.value = value
        self.schema = schema
        self.machine_set = machine_set
        self.visibility = visibility
        self.opacity = opacity
        self.color = self.calculate_color()

    def calculate_color(self):
        if not self.visibility:
            return None  # Transparent if not visible

        # Multi-dimensional color scheme
        hue = (self.value * 36) % 360
        lightness = 0.5 * (1 + ((self.value % 3) - 1) / 2)
        saturation = self.opacity  # Use opacity as saturation

        if self.schema == 'schema1':
            hue += 50
            lightness += 0.1
        elif self.schema == 'schema2':
            hue += 100

        if self.machine_set == 'set1':
            lightness -= 0.1
        elif self.machine_set == 'set2':
            saturation += 0.1

        r, g, b = colorsys.hls_to_rgb(hue / 360, lightness, saturation)
        return f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'


class ResonanceGrid:
    def __init__(self, matrix):
        self.grid = [[Cell(value) for value in row] for row in matrix]
        self.current_frequency = 1
        self.memoization = {}
        self.image_counter = 0

    def display(self, canvas):
        cell_size = 10
        canvas_width = len(self.grid[0]) * cell_size
        canvas_height = len(self.grid) * cell_size
        canvas.config(width=canvas_width, height=canvas_height)
        for x, row in enumerate(self.grid):
            for y, cell in enumerate(row):
                if cell.color:
                    canvas.create_rectangle(y * cell_size, x * cell_size,
                                            (y + 1) *
                                            cell_size, (x + 1) * cell_size,
                                            fill=cell.color, outline='')

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

    def apply_resonance(self, frequency, root):
        if frequency not in self.memoization:
            for row in self.grid:
                for cell in row:
                    cell.value = (cell.value + frequency) % 10
                    cell.color = cell.calculate_color()

            self.save_grid_state_as_image(frequency)

            self.memoization[frequency] = [[cell for cell in row]
                                           for row in self.grid]

        avg_color = self.average_color()
        root.title(
            f"Resonance Grid - Freq: {frequency}, Avg Color: {avg_color}")

    def save_grid_state_as_image(self, frequency):
        cell_size = 10
        image_width = len(self.grid[0]) * cell_size
        image_height = len(self.grid) * cell_size
        image = Image.new('RGBA', (image_width, image_height),
                          (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)

        for x, row in enumerate(self.grid):
            for y, cell in enumerate(row):
                if cell.color:
                    x0, y0 = y * cell_size, x * cell_size
                    x1, y1 = x0 + cell_size, y0 + cell_size
                    draw.rectangle(
                        [x0, y0, x1, y1], fill=cell.color + f'{int(cell.opacity * 255):02x}')

        image.save(f"grid_state_{frequency}_{self.image_counter}.png")
        self.image_counter += 1

    def list_seen_images(self):
        for freq, _ in self.memoization.items():
            print(
                f"Frequency: {freq}, Image: grid_state_{freq}_{self.image_counter}.png")


def main():
    root = tk.Tk()
    root.title("Resonance Grid Simulation")
    base_grid = pd.read_csv('a.csv', header=None).values.tolist()

    resonance_grid = ResonanceGrid(base_grid)

    canvas = tk.Canvas(root)
    canvas.pack()

    def redraw():
        canvas.delete("all")
        resonance_grid.display(canvas)

    def on_click(event):
        frequency = random.randint(1, 9)
        resonance_grid.apply_resonance(frequency, root)
        redraw()

    canvas.bind("<Button-1>", on_click)
    redraw()

    def list_images():
        resonance_grid.list_seen_images()

    list_button = tk.Button(root, text="List Seen Images", command=list_images)
    list_button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
