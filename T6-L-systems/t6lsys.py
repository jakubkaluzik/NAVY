import tkinter as tk
from tkinter import ttk, messagebox
import math

class LSystemGenerator:
    # Initialization of the L-system generator
    def __init__(self, root):
        self.root = root
        self.root.title("L-System Generator")
        
        # Color theme
        self.bg_color = "#00264d"
        self.fg_color = "#ffffff"
        self.input_bg = "#002e5c"
        self.button_bg = "#004080"
        self.canvas_bg = "#001a33"
        self.entry_width = 15

        self.font = ("Arial", 10)
        
        # Default templates
        # Each template has a name, axiom, rule, angle, and angle type
        self.templates = [
            {"name": "Template 1", "axiom": "F+F+F+F", "rule": "F -> F+F-F-FF+F+F-F", "angle": 90, "angle_type": "degrees"},
            {"name": "Template 2", "axiom": "F++F++F", "rule": "F -> F+F--F+F", "angle": 60, "angle_type": "degrees"},
            {"name": "Template 3", "axiom": "F", "rule": "F -> F[+F]F[-F]F", "angle": math.pi/7, "angle_type": "radians"},
            {"name": "Template 4", "axiom": "F", "rule": "F -> FF+[+F-F-F]-[-F+F+F]", "angle": math.pi/8, "angle_type": "radians"},
            {"name": "Template 5", "axiom": "F+F+F", "rule": "F -> F-F+F", "angle": 120, "angle_type": "degrees"},
            {"name": "Template 6", "axiom": "F+F+F+F", "rule": "F -> FF+F++F+F", "angle": 90, "angle_type": "degrees"},
            {"name": "Template 7", "axiom": "F++F++F", "rule": "F -> F-F++F-F", "angle": 60, "angle_type": "degrees"},
            {"name": "Template 8", "axiom": "F", "rule": "F -> F-F+F+F-F", "angle": 90, "angle_type": "degrees"},
            {"name": "Template 9", "axiom": "F+F+F+F", "rule": "F -> FF+F+F+F+F+F-F", "angle": 90, "angle_type": "degrees"},
            {"name": "Template 10", "axiom": "F", "rule": "F -> F[+FF][-FF]F[-F][+F]F", "angle": math.pi/5, "angle_type": "radians"},
            {"name": "Template 11", "axiom": "F++F++F+++F--F--F", "rule": "F -> FF++F++F++FFF", "angle": 60, "angle_type": "degrees"}
        ]
    
    # Canvas and controls
    def create_main_layout(self):
        self.control_frame = tk.Frame(self.root, bg=self.bg_color, padx=15, pady=15)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas_frame = tk.Frame(self.root, bg=self.bg_color, padx=15, pady=15)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_canvas()
    
    def create_canvas(self):
        self.canvas = tk.Canvas(self.canvas_frame, bg=self.canvas_bg, width=600, height=500)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def clear_canvas(self):
        self.canvas.delete("all")
        
    # Sets the styles of widgets
    def set_style(self):
        style = ttk.Style()
        style.configure("TLabel", background=self.bg_color, foreground=self.fg_color, font=self.font)
        style.configure("TEntry", background=self.input_bg, foreground=self.fg_color, fieldbackground=self.input_bg)
        style.configure("TButton", background=self.button_bg, foreground=self.fg_color, font=self.font)
        style.map("TButton", background=[("active", "#005cb3")])
        style.configure("TCombobox", foreground="#000000", fieldbackground=self.fg_color)
        style.map("TCombobox", fieldbackground=[("readonly", self.fg_color)])

    # Every define_uinput creates its own frame and packs it into the control frame
    # Entry fields for starting position
    def define_uinput_position(self):
        pos_frame = tk.Frame(self.control_frame, bg=self.bg_color, pady=5)
        pos_frame.pack(fill=tk.X)
        
        col1 = tk.Frame(pos_frame, bg=self.bg_color)
        col1.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        tk.Label(col1, text="Starting X Position", bg=self.bg_color, fg=self.fg_color, font=self.font).pack(anchor="w", pady=(0, 5))
        self.x_pos = tk.StringVar(value="150")
        x_entry = tk.Entry(col1, textvariable=self.x_pos, bg=self.input_bg, fg=self.fg_color, width=self.entry_width)
        x_entry.pack(fill=tk.X)
        
        col2 = tk.Frame(pos_frame, bg=self.bg_color)
        col2.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        tk.Label(col2, text="Starting Y Position", bg=self.bg_color, fg=self.fg_color, font=self.font).pack(anchor="w", pady=(0, 5))
        self.y_pos = tk.StringVar(value="100")
        y_entry = tk.Entry(col2, textvariable=self.y_pos, bg=self.input_bg, fg=self.fg_color, width=self.entry_width)
        y_entry.pack(fill=tk.X)

    # Entry fields for starting angle and angle type (degrees/radians)
    def define_uinput_angle(self):
        angle_frame = tk.Frame(self.control_frame, bg=self.bg_color, pady=5)
        angle_frame.pack(fill=tk.X)
        
        col1 = tk.Frame(angle_frame, bg=self.bg_color)
        col1.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        tk.Label(col1, text="Starting Angle", bg=self.bg_color, fg=self.fg_color, font=self.font).pack(anchor="w", pady=(0, 5))
        self.angle = tk.StringVar(value="0")
        angle_entry = tk.Entry(col1, textvariable=self.angle, bg=self.input_bg, fg=self.fg_color, width=self.entry_width)
        angle_entry.pack(fill=tk.X)
        
        col2 = tk.Frame(angle_frame, bg=self.bg_color)
        col2.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        tk.Label(col2, text="Angle Type", bg=self.bg_color, fg=self.fg_color, font=self.font).pack(anchor="w", pady=(0, 5))
        self.angle_type = tk.StringVar(value="degrees")
        angle_type_combo = ttk.Combobox(col2, textvariable=self.angle_type, values=["degrees", "radians"], width=self.entry_width-2, state="readonly")
        angle_type_combo.pack(fill=tk.X)

    # Entry fields for number of iterations and line size
    def define_uinput_parameters(self):
        params_frame = tk.Frame(self.control_frame, bg=self.bg_color, pady=5)
        params_frame.pack(fill=tk.X)
        
        col1 = tk.Frame(params_frame, bg=self.bg_color)
        col1.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        tk.Label(col1, text="Number of Iterations", bg=self.bg_color, fg=self.fg_color, font=self.font).pack(anchor="w", pady=(0, 5))
        self.iterations = tk.StringVar(value="3")
        iterations_entry = tk.Entry(col1, textvariable=self.iterations, bg=self.input_bg, fg=self.fg_color, width=self.entry_width)
        iterations_entry.pack(fill=tk.X)
        
        col2 = tk.Frame(params_frame, bg=self.bg_color)
        col2.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        tk.Label(col2, text="Line Size", bg=self.bg_color, fg=self.fg_color, font=self.font).pack(anchor="w", pady=(0, 5))
        self.line_size = tk.StringVar(value="5")
        line_size_entry = tk.Entry(col2, textvariable=self.line_size, bg=self.input_bg, fg=self.fg_color, width=self.entry_width)
        line_size_entry.pack(fill=tk.X)

    # The axiom, rule, and angle type are set to the first template by default
    # The template dropdown allows the user to select a different template
    # Fields are not editable
    def define_uinput_templates(self):
        template_frame = tk.Frame(self.control_frame, bg=self.bg_color, pady=5)
        template_frame.pack(fill=tk.X)

        tk.Label(template_frame, text="Templates", bg=self.bg_color, fg=self.fg_color, font=self.font).pack(anchor="w", pady=(0, 5))
        self.template_var = tk.StringVar(value="Template 1")  # Default to first template
        templates = [t["name"] for t in self.templates]
        self.template_combo = ttk.Combobox(template_frame, textvariable=self.template_var, values=templates, width=self.entry_width*2+3, state="readonly")
        self.template_combo.pack(fill=tk.X)
        self.template_combo.bind("<<ComboboxSelected>>", self.load_template)

        lsys_frame = tk.Frame(self.control_frame, bg=self.bg_color, pady=5)
        lsys_frame.pack(fill=tk.X)

        tk.Label(lsys_frame, text="Axiom", bg=self.bg_color, fg=self.fg_color, font=self.font).pack(anchor="w", pady=(0, 5))
        self.axiom = tk.StringVar(value=self.templates[0]["axiom"])
        axiom_label = tk.Label(lsys_frame, textvariable=self.axiom, bg=self.input_bg, fg=self.fg_color, font=self.font, anchor="w", padx=5)
        axiom_label.pack(fill=tk.X)

        rule_frame = tk.Frame(self.control_frame, bg=self.bg_color, pady=5)
        rule_frame.pack(fill=tk.X)

        tk.Label(rule_frame, text="Rule", bg=self.bg_color, fg=self.fg_color, font=self.font).pack(anchor="w", pady=(0, 5))
        self.rule = tk.StringVar(value=self.templates[0]["rule"])
        rule_label = tk.Label(rule_frame, textvariable=self.rule, bg=self.input_bg, fg=self.fg_color, font=self.font, anchor="w", padx=5)
        rule_label.pack(fill=tk.X)

        l_angle_frame = tk.Frame(self.control_frame, bg=self.bg_color, pady=5)
        l_angle_frame.pack(fill=tk.X)

        col1 = tk.Frame(l_angle_frame, bg=self.bg_color)
        col1.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        tk.Label(col1, text="L-system Angle", bg=self.bg_color, fg=self.fg_color, font=self.font).pack(anchor="w", pady=(0, 5))
        self.l_angle = tk.StringVar(value=str(self.templates[0]["angle"]))
        l_angle_label = tk.Label(col1, textvariable=self.l_angle, bg=self.input_bg, fg=self.fg_color, font=self.font, anchor="w", padx=5)
        l_angle_label.pack(fill=tk.X)

        col2 = tk.Frame(l_angle_frame, bg=self.bg_color)
        col2.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        tk.Label(col2, text="Angle Type", bg=self.bg_color, fg=self.fg_color, font=self.font).pack(anchor="w", pady=(0, 5))
        self.l_angle_type = tk.StringVar(value=self.templates[0]["angle_type"])
        l_angle_type_label = tk.Label(col2, textvariable=self.l_angle_type, bg=self.input_bg, fg=self.fg_color, font=self.font, anchor="w", padx=5)
        l_angle_type_label.pack(fill=tk.X)

    # Main control buttons for drawing, clearing canvas, and creating new templates
    def define_uinput_control_buttons(self):
        button_frame = tk.Frame(self.control_frame, bg=self.bg_color, pady=10)
        button_frame.pack(fill=tk.X)
        
        button_width = self.entry_width*2+5
        
        draw_btn = tk.Button(button_frame, text="Draw", font=self.font, bg=self.button_bg, fg=self.fg_color,
                             width=button_width, borderwidth=0, relief="flat", activebackground="#005cb3",
                             command=self.draw_lsystem)
        draw_btn.pack(pady=5)
        
        clear_btn = tk.Button(button_frame, text="Clear Canvas", font=self.font, bg="#800000", fg=self.fg_color,
                              width=button_width, borderwidth=0, relief="flat", activebackground="#b30000",
                              command=self.clear_canvas)
        clear_btn.pack(pady=5)

    # Fucntion for option menu to load the selected template
    def load_template(self, event=None):
        selected = self.template_var.get()

        for template in self.templates:
            if template["name"] == selected:
                self.axiom.set(template["axiom"])
                self.rule.set(template["rule"])
                self.l_angle.set(str(template["angle"]))
                self.l_angle_type.set(template["angle_type"])
                break

#L-sytem logic-----------------------------------------------------------------------------------------
    # This function generates the L-system string based on the axiom and rules
    # It is based on the number of iterations specified by the user
    def generate_lsystem(self, axiom, rules, iterations):
        result = axiom       
        for _ in range(iterations):
            new_result = ""
            for char in result:
                if char in rules:
                    new_result += rules[char]
                else:
                    new_result += char
            result = new_result
            
        return result
    
    def interpret_draw_lsystem(self, commands, x, y, length, start_angle, angle):
        # Initialize position and angle
        pos_x, pos_y = x, y
        current_angle = start_angle
        
        # Stack for saving positions and angles (its for checkpoints)
        stack = []
        
        # Main loop for drawing the L-system
        # Iterates through each command in the L-system string
        # F = move forward, + = turn right, - = turn left, [ = checkpoint, ] = go back to checkpoint
        for cmd in commands:
            if cmd == 'F':
                new_x = pos_x + length * math.cos(current_angle)
                new_y = pos_y + length * math.sin(current_angle)
                
                self.canvas.create_line(pos_x, pos_y, new_x, new_y, fill=self.fg_color, width=1)
                
                pos_x, pos_y = new_x, new_y
            elif cmd == '+':
                current_angle += angle
                
            elif cmd == '-':
                current_angle -= angle
                
            elif cmd == '[':
                stack.append((pos_x, pos_y, current_angle))
                
            elif cmd == ']':
                if stack:
                    pos_x, pos_y, current_angle = stack.pop()

    # This function parses the L-system string and interprets it to draw on the canvas
    # Its called when the user clicks the Draw button is pressed
    def draw_lsystem(self):
        # Clear the canvas before drawing
        self.clear_canvas()
    
        try:
            # Get parameters from UI
            x_pos = float(self.x_pos.get())
            y_pos = float(self.y_pos.get())
            iterations = int(self.iterations.get())
            line_size = float(self.line_size.get())
            start_angle = float(self.angle.get())

            if self.angle_type.get() == "degrees":
                start_angle = math.radians(start_angle)
            
            # Parse rule
            rule_text = self.rule.get()
            rules = {}
            for rule in rule_text.split(","):
                rule = rule.strip()
                if "->" in rule:
                    parts = rule.split("->")
                    if len(parts) == 2:
                        symbol = parts[0].strip()
                        replacement = parts[1].strip()
                        rules[symbol] = replacement
            
            # Get L-system parameters
            axiom = self.axiom.get()
            angle = float(self.l_angle.get())
            
            if self.l_angle_type.get() == "degrees":
                angle = math.radians(angle)

            # Generate the L-system string
            result = self.generate_lsystem(axiom, rules, iterations)
            
            # Draw the L-system
            self.interpret_draw_lsystem(result, x_pos, y_pos, line_size, start_angle, angle)
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
#-----------------------------------------------------------------------------------------

    # Function that calls all of the specified uinput functions
    def create_controls(self):

        self.set_style()
        
        self.define_uinput_position()
        
        self.define_uinput_angle()

        self.define_uinput_parameters()

        self.define_uinput_templates()

        self.define_uinput_control_buttons()
        
    # Main function to run the application
    def run(self):
        self.root.configure(bg=self.bg_color)

        self.create_main_layout()

        self.create_controls()

root = tk.Tk()
app = LSystemGenerator(root)
app.run()
root.mainloop()