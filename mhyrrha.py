import time
import threading
import tkinter as tk
import random
import hashlib
import colorsys
import pandas as pd


# Improved CommiphoraMyrrha class with more detailed visuals


class CommiphoraMyrrha:
    def __init__(self, canvas):
        self.age = 0
        self.health = 100
        self.resin = 0
        self.growing = False
        self.canvas = canvas
        self.tree_id = None

    def start_growing(self):
        self.growing = True
        threading.Thread(target=self.grow, daemon=True).start()

    def grow(self):
        while self.growing:
            time.sleep(1)
            self.age += 1
            self.health -= 1
            self.resin += 5
            self.update_display()
            if self.health <= 0:
                self.growing = False
                print("The tree has stopped growing due to poor health.")

    def update_display(self):
        if self.tree_id:
            self.canvas.delete(self.tree_id)
        tree_height = max(10, min(100, self.age * 2))
        tree_width = max(5, min(50, self.age))
        self.tree_id = self.canvas.create_rectangle(
            250 - tree_width // 2, 300 - tree_height,
            250 + tree_width // 2, 300,
            fill="#8B4513"  # Brown color for the tree
        )

# Cell class as before


class Cell:
    def __init__(self, value):
        self.value = value
        self.color = self.calculate_color()

    def calculate_color(self):
        hue = (self.value * 36) % 360
        r, g, b = colorsys.hls_to_rgb(hue / 360, 0.5, 1)
        return f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'

    # ... (same as before)

# Enhanced ResonanceGrid class to reflect tree health in color patterns


class ResonanceGrid:
    def __init__(self, tree, canvas):
        self.tree = tree
        self.canvas = canvas
        self.grid = [[Cell(0) for _ in range(10)] for _ in range(10)]
        self.update_grid()

    def update_grid(self):
        health_factor = self.tree.health / 100
        for row in self.grid:
            for cell in row:
                cell.value = random.randint(0, 9) * health_factor
                cell.color = cell.calculate_color()
        self.display()

    def display(self):
        cell_size = 30
        self.canvas.delete("all")
        for x, row in enumerate(self.grid):
            for y, cell in enumerate(row):
                self.canvas.create_rectangle(
                    y * cell_size, x * cell_size,
                    (y + 1) * cell_size, (x + 1) * cell_size,
                    fill=cell.color, outline=''
                )

    def calculate_proof_of_work(self):
        grid_color = ''.join([cell.color for row in self.grid for cell in row])
        hash_object = hashlib.sha256(grid_color.encode())
        hash_hex = hash_object.hexdigest()
        return hash_hex[:5] == '00000'  # Simplified proof of work

# Main function


def main():
    root = tk.Tk()
    root.title("Commiphora Myrrha Growth and Resonance Grid Simulation")

    tree_canvas = tk.Canvas(root, width=500, height=300)
    tree_canvas.pack()

    grid_canvas = tk.Canvas(root, width=300, height=300)
    grid_canvas.pack()

    my_tree = CommiphoraMyrrha(tree_canvas)
    my_tree.start_growing()

    resonance_grid = ResonanceGrid(my_tree, grid_canvas)

    def on_click():
        resonance_grid.update_grid()
        proof_of_work = resonance_grid.calculate_proof_of_work()
        print(f"Proof of Work Achieved: {proof_of_work}")

    button = tk.Button(root, text="Update Grid", command=on_click)
    button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
