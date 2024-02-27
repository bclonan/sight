import colorsys
import random

import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class Ulid:  # A simple ULID generator
    def __init__(self):
        self.counter = 0

    def new(self):
        self.counter += 1
        return f"00000000-0000-0000-0000-{self.counter:012x}"

ulid = Ulid()

class Cell:
    def __init__(self, value):
        self.id = ulid.new()
        self.value = value
        self.color = self.calculate_color()

    def calculate_color(self):
        hue = (self.value * 36) % 360
        r, g, b = colorsys.hls_to_rgb(hue / 360, 0.5, 1)
        return f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'

    def set_value(self, new_value):
        self.value = new_value
        self.color = self.calculate_color()

class GridManager:
    def __init__(self, matrix):
        self.grid = [[Cell(value) for value in row] for row in matrix]

    def apply_resonance(self, frequency):
        for row in self.grid:
            for cell in row:
                new_value = (cell.value + frequency) % 10
                cell.set_value(new_value)

    def get_grid_state(self):
        flat_grid = [cell for row in self.grid for cell in row]
        color_codes = {cell.id: cell.color for cell in flat_grid}
        average_color = self.calculate_average_color(flat_grid)
        return color_codes, average_color

    def calculate_average_color(self, cells):
        num_cells = len(cells)
        if num_cells == 0:
            return '#000000'
        total_r = total_g = total_b = 0
        for cell in cells:
            hex_color = cell.color.lstrip('#')
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            total_r += r
            total_g += g
            total_b += b
        avg_r = int(total_r / num_cells)
        avg_g = int(total_g / num_cells)
        avg_b = int(total_b / num_cells)
        return f'#{avg_r:02x}{avg_g:02x}{avg_b:02x}'

# Initialize grid manager with dummy data
try:
    base_grid = pd.read_csv('a.csv', header=None).values.tolist()
except FileNotFoundError:
    base_grid = [[random.randint(0, 9) for _ in range(10)] for _ in range(10)]  # Adjusted to 10x10 for simplicity

grid_manager = GridManager(base_grid)

@app.route('/click', methods=['POST'])
def handle_click():
    data = request.json
    print(data)
    frequency = data.get('frequency', 1)  # Default frequency to 1 if not provided
    grid_manager.apply_resonance(frequency)
    return jsonify(success=True)

@app.route('/grid', methods=['GET'])
def get_grid():
    color_codes, average_color = grid_manager.get_grid_state()
    return jsonify({
        'color_codes': color_codes,
        'average_color': average_color
    })
    
@app.route('/', methods=['GET'])
def index():
    # generate the grid and return the color codes and average color
    color_codes, average_color = grid_manager.get_grid_state()
    return jsonify({
        'color_codes': color_codes,
        'average_color': average_color
    })
    
    
    

if __name__ == '__main__':
    app.run(debug=True)
