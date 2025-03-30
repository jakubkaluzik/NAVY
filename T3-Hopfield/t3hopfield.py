# !!! IMPORATNT INFO !!!
# The async repair visualizes the repair process, pattern will most of the times be repaired before all iterations are done
# U can see the progress at the right bottom side of the window
# During the training or repairing, inputs are ignored so u can't change the pattern etc.

import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np
import threading
import time

# Hopfield Network implementation
class HopfieldNetwork:
    # Initializes the Hopfield network with a given size and sets the weights to zero.
    def __init__(self, size):
        self.size = size
        self.weights = np.zeros((size, size))
    
    # Trains the network for a set of patterns by calculating the outer product of each pattern with itself and summing them up.
    def train(self, patterns):
        self.weights = np.zeros((self.size, self.size))
        for pattern in patterns:
            pattern = np.array(pattern)
            outer_product = np.outer(pattern, pattern)
            np.fill_diagonal(outer_product, 0)
            self.weights += outer_product
        if len(patterns) > 0:
            self.weights /= len(patterns)
    
    # Updates the network with a given pattern by iterating through the neurons and updating their states based on the weighted sum of their inputs.
    # The process continues until the pattern stabilizes or the maximum number of iterations is reached.
    def update(self, pattern, max_iterations=10):
        pattern = np.array(pattern)
        prev_pattern = np.zeros_like(pattern)
        for _ in range(max_iterations):
            prev_pattern = pattern.copy()
            for i in range(self.size):
                activation = np.dot(self.weights[i], pattern)
                pattern[i] = 1 if activation > 0 else -1
            if np.array_equal(pattern, prev_pattern):
                break
        return pattern
    
# GridApp class to create the GUI for the Hopfield network pattern editor
class GridApp:
    # Initializes the GridApp with a root window, grid size, and cell size. It sets up the canvas, buttons, and status bar.
    # It also initializes the Hopfield network and sets up the grid for the patterns.
    def __init__(self, root, grid_size=12, cell_size=36):
        self.root = root
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.saved_patterns = []
        self.hopfield = HopfieldNetwork(grid_size * grid_size)
        self.processing = False

        self.root.configure(bg="#1E1E2E")
        
        self.canvas = tk.Canvas(root, width=grid_size * cell_size, height=grid_size * cell_size, bg='#2A2A40', highlightthickness=2, relief="ridge")
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#1E1E2E", fg="white", width=50)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.canvas.bind("<Button-1>", self.toggle_cell)
        
        self.buttons_frame = tk.Frame(root, bg="#1E1E2E")
        self.buttons_frame.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        self.create_buttons()
        self.draw_grid()
    
    # Creates the buttons for saving, repairing, showing, and clearing patterns.
    # It also sets the styles for the buttons and adds them to the buttons frame.
    def create_buttons(self):
        style = ttk.Style()
        style.configure("TButton", padding=6, font=("Arial", 10), background="#1E1E2E", foreground="black")
        
        btn_save = ttk.Button(self.buttons_frame, text="Save Pattern", command=self.save_pattern, style="TButton", width=20)
        btn_save.pack(fill=tk.X, pady=5)
        
        btn_repair_sync = ttk.Button(self.buttons_frame, text="Repair Pattern (Sync)", command=self.repair_pattern_sync, style="TButton", width=20)
        btn_repair_sync.pack(fill=tk.X, pady=5)
        
        btn_repair_async = ttk.Button(self.buttons_frame, text="Repair Pattern (Async)", command=self.repair_pattern_async, style="TButton", width=20)
        btn_repair_async.pack(fill=tk.X, pady=5)
        
        btn_show = ttk.Button(self.buttons_frame, text="Show Saved Patterns", command=self.show_patterns, style="TButton", width=20)
        btn_show.pack(fill=tk.X, pady=5)
        
        btn_clear = ttk.Button(self.buttons_frame, text="Clear Grid", command=self.clear_grid, style="TButton", width=20)
        btn_clear.pack(fill=tk.X, pady=5)
        
        self.info_label = tk.Label(self.buttons_frame, text="Max recommended saved patterns: 5", font=("Arial", 9), bg="#1E1E2E", fg="white")
        self.info_label.pack(pady=10)
    
    # Draws the grid on the canvas by creating rectangles for each cell and storing their IDs in a dictionary.
    def draw_grid(self):
        self.cells = {}
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x1, y1 = col * self.cell_size, row * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                cell_id = self.canvas.create_rectangle(x1, y1, x2, y2, outline='#4A4A6A', fill='#2A2A40')
                self.cells[(row, col)] = cell_id
    
    # Toggles the color of a cell when clicked. It changes the fill color of the rectangle based on its current state.
    def toggle_cell(self, event):
        if self.processing:
            return
        row, col = event.y // self.cell_size, event.x // self.cell_size
        cell_id = self.cells.get((row, col))
        if cell_id:
            current_color = self.canvas.itemcget(cell_id, "fill")
            new_color = "#E0E0E0" if current_color == "#2A2A40" else "#2A2A40"
            self.canvas.itemconfig(cell_id, fill=new_color)
    
    # Gets the current pattern from the grid by checking the fill color of each cell and returning a numpy array of 1s and -1s.
    # 1 represents a filled cell and -1 represents an empty cell.
    def get_current_pattern(self):
        pattern = []
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                cell_id = self.cells[(row, col)]
                value = 1 if self.canvas.itemcget(cell_id, "fill") == "#E0E0E0" else -1
                pattern.append(value)
        return np.array(pattern)
    
    # Updates the grid from a given pattern by iterating through the pattern and changing the fill color of each cell accordingly.
    def update_grid_from_pattern(self, pattern):
        idx = 0
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                cell_id = self.cells[(row, col)]
                fill_color = "#E0E0E0" if pattern[idx] == 1 else "#2A2A40"
                self.canvas.itemconfig(cell_id, fill=fill_color)
                idx += 1
    
    # Saves the current pattern to the Hopfield network and trains it. 
    # It checks for duplicates and ensures that the maximum number of saved patterns is not exceeded.
    def save_pattern(self):
        if self.processing:
            return
        pattern = self.get_current_pattern()
        if np.sum(pattern == 1) == 0:
            messagebox.showwarning("Empty Pattern", "Cannot save an empty pattern!")
            return
        for saved_pattern in self.saved_patterns:
            if np.array_equal(pattern, saved_pattern):
                messagebox.showwarning("Duplicate Pattern", "This pattern is already saved!")
                return
        if len(self.saved_patterns) >= 5:
            messagebox.showwarning("Limit Reached", "Max recommended saved patterns is 5!")
        else:
            self.saved_patterns.append(pattern)
            self.status_var.set("Training network...")
            self.root.update()
            self.hopfield.train(self.saved_patterns)
            self.status_var.set(f"Network trained with {len(self.saved_patterns)} pattern(s)")
            messagebox.showinfo("Saved", f"Pattern {len(self.saved_patterns)} saved and network trained!")
    
    # Repairs the current pattern using the Hopfield network synchronously.
    # It updates the grid with the repaired pattern and handles any errors that may occur during the process.
    def repair_pattern_sync(self):
        if self.processing:
            return
        if not self.saved_patterns:
            messagebox.showwarning("No Patterns", "Please save at least one pattern first!")
            return
        self.processing = True
        self.status_var.set("Repairing pattern...")
        self.root.update()
        try:
            current_pattern = self.get_current_pattern()
            repaired_pattern = self.hopfield.update(current_pattern)
            self.update_grid_from_pattern(repaired_pattern)
            self.status_var.set("Pattern repaired")
        except Exception as e:
            messagebox.showerror("Error", f"Error during repair: {str(e)}")
            self.status_var.set("Error during repair")
        finally:
            self.processing = False
    
    def repair_pattern_async(self):
        if self.processing:
            return
        if not self.saved_patterns:
            messagebox.showwarning("No Patterns", "Please save at least one pattern first!")
            return
        self.processing = True
        threading.Thread(target=self._async_repair).start()
    
    # Repairs the current pattern using the Hopfield network asynchronously.
    # It updates the grid with the repaired pattern and visualizes the iterations.
    # It handles any errors that may occur during the process.
    # Sleeps for a short duration to allow the GUI to update and show the iterations.
    def _async_repair(self):
        self.status_var.set("Repairing pattern (visualizing iterations)...")
        self.root.update()
        try:
            current_pattern = self.get_current_pattern()
            pattern = current_pattern.copy()
            prev_pattern = np.zeros_like(pattern)
            for iteration in range(10):
                prev_pattern = pattern.copy()
                for i in range(len(pattern)):
                    activation = np.dot(self.hopfield.weights[i], pattern)
                    pattern[i] = 1 if activation > 0 else -1
                    if i % 10 == 0:
                        self.root.after(0, lambda p=pattern.copy(): self.update_grid_from_pattern(p))
                        time.sleep(0.1)
                self.root.after(0, lambda p=pattern.copy(): self.update_grid_from_pattern(p))
                time.sleep(1.0)
                if np.array_equal(pattern, prev_pattern):
                    break
            self.root.after(0, lambda: self.status_var.set("Pattern repair complete"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error during repair: {str(e)}"))
            self.root.after(0, lambda: self.status_var.set("Error during repair"))
        finally:
            self.root.after(0, lambda: setattr(self, 'processing', False))
    
    # Shows the saved patterns in a new window. It creates a canvas for each saved pattern and displays it.
    # It also provides a button to load the pattern back into the main grid.
    def show_patterns(self):
        if not self.saved_patterns:
            messagebox.showinfo("Saved Patterns", "No saved patterns.")
            return
        patterns_window = tk.Toplevel(self.root)
        patterns_window.title("Saved Patterns")
        patterns_window.configure(bg="#1E1E2E")
        small_size = 20
        for i, pattern in enumerate(self.saved_patterns):
            frame = tk.Frame(patterns_window, bg="#1E1E2E", padx=10, pady=10)
            frame.grid(row=i//3, column=i%3, padx=10, pady=10)
            label = tk.Label(frame, text=f"Pattern {i+1}", bg="#1E1E2E", fg="white")
            label.pack()
            canvas = tk.Canvas(frame, width=self.grid_size * small_size, 
                              height=self.grid_size * small_size, 
                              bg='#2A2A40')
            canvas.pack()
            idx = 0
            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    x1, y1 = col * small_size, row * small_size
                    x2, y2 = x1 + small_size, y1 + small_size
                    fill_color = "#E0E0E0" if pattern[idx] == 1 else "#2A2A40"
                    canvas.create_rectangle(x1, y1, x2, y2, outline='#4A4A6A', fill=fill_color)
                    idx += 1
            load_btn = ttk.Button(frame, text="Load", 
                                 command=lambda p=pattern, w=patterns_window: self.load_pattern(p, w))
            load_btn.pack(pady=5)
    
    def load_pattern(self, pattern, window):
        self.update_grid_from_pattern(pattern)
        window.destroy()
    
    # Clears the grid by resetting the fill color of each cell to its default state.
    # It ensures that the grid is not being processed before clearing it.
    def clear_grid(self):
        if self.processing:
            return
        for cell_id in self.cells.values():
            self.canvas.itemconfig(cell_id, fill="#2A2A40")

# Main function to run the application
# It creates the main window and initializes the GridApp.
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Hopfield Network Pattern Repairer")
    root.resizable(False, False)
    app = GridApp(root)
    root.mainloop()