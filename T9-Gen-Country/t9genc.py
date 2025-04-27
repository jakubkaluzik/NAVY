# IMPORTANT !!!
# It is basic program for generating 3 random terrain layers using fractal terrain generation.
# The have spefic colors and heights.
import tkinter as tk
import random

class FractalTerrain2D:
    def __init__(self, root):
        self.root = root
        self.root.title("GEN OF 2D COUNTRY")
        self.canvas = tk.Canvas(root, width=900, height=600, bg='white')
        self.canvas.pack(side=tk.LEFT)
        control_frame = tk.Frame(root)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.num_iterations = tk.IntVar(value=8)
        self.offset = tk.DoubleVar(value=100.0)
        tk.Label(control_frame, text="Number of iterations:").pack()
        tk.Entry(control_frame, textvariable=self.num_iterations).pack()
        tk.Label(control_frame, text="Offset:").pack()
        tk.Entry(control_frame, textvariable=self.offset).pack()
        tk.Button(control_frame, text="Draw Terrain", command=self.draw_terrain).pack(pady=10)
        tk.Button(control_frame, text="Clear Canvas", command=self.clear_canvas).pack()

    def spatial_subdivision(self, x1, x2, y1, y2, iterations, offset, points):
        if iterations == 0:
            return
        split_x = (x1 + x2) / 2
        split_y = (y1 + y2) / 2 + random.uniform(-offset, offset)
        points[split_x] = split_y
        self.spatial_subdivision(x1, split_x, y1, split_y, iterations - 1, offset / 2, points)
        self.spatial_subdivision(split_x, x2, split_y, y2, iterations - 1, offset / 2, points)

    def generate_terrain(self, width, start_height, end_height, iterations, offset, seed=None):
        if seed is not None:
            random.seed(seed)
        points = {0: start_height, width: end_height}
        self.spatial_subdivision(0, width, start_height, end_height, iterations, offset, points)
        return [(x, points[x]) for x in sorted(points.keys())]

    def draw_terrain(self):
        self.clear_canvas()
        width = int(self.canvas['width'])
        height = int(self.canvas['height'])
        iterations = min(max(self.num_iterations.get(), 1), 8)
        offset = min(max(self.offset.get(), 10.0), 200.0)
        # 3 layers of terrain, each with different colors and heights
        layers = [
            {"start_height": height * 0.7, "end_height": height * 0.7, "color": "#228B22", "roughness": offset},
            {"start_height": height * 0.5, "end_height": height * 0.5, "color": "#8B4513", "roughness": offset * 0.8},
            {"start_height": height * 0.3, "end_height": height * 0.3, "color": "#DCDCDC", "roughness": offset * 0.6},
        ]
        # Draw each layer of terrain
        for layer in reversed(layers):
            terrain_points = self.generate_terrain(width, layer["start_height"], layer["end_height"], iterations, layer["roughness"])
            polygon_points = [(0, height)] + terrain_points + [(width, height)]
            self.canvas.create_polygon(polygon_points, fill=layer["color"], outline="")

    def clear_canvas(self):
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = FractalTerrain2D(root)
    app.draw_terrain()
    root.mainloop()