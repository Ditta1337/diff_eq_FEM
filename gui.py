import tkinter as tk
from tkinter import messagebox
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasAgg
import numpy as np
from PIL import Image, ImageTk
from solution import get_solution

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gravitational potential - FEM")
        self.root.geometry("600x400")
        self.root.resizable(0, 0)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        plt.rcParams['text.latex.preamble'] = r"\usepackage{amsmath}"
        self.latex_to_image(
            r"\begin{gather*}"
            r"\Large{\textbf{Gravitational potential}} \\\\"
            r"\frac{d^2 \phi}{d x^2} = 4 \pi G \rho(x) \\"
            r"\phi(0) = 5 \\"
            r"\phi(3) = 7 \\"
            r"\rho(x) = \begin{cases} 0 \text{ for } x \in [0, 1] \\ 1 \text{ for } x \in (1, 2] \\ 0 \text{ for } x \in (2, 3] \end{cases} \\" 
            r"\text{Assume } G = 1"
            r"\end{gather*}"
        )
        image = tk.PhotoImage(file="./latex.png")
    
        self.label = tk.Label(self.root, image=image)
        self.label.pack()

        self.label = tk.Label(self.root, text="Number of elements:")
        self.label.pack()

        self.entry = tk.Entry(self.root, justify="center")
        self.entry.insert(0, "1000")
        self.entry.pack()

        self.button = tk.Button(self.root, text="Start", command=self.start)
        self.button.pack()

        self.root.mainloop()

    def on_closing(self):
        self.root.destroy()

    def latex_to_image(self, latex_formula):
        mpl.rcParams['text.usetex'] = True

        fig = plt.figure(2, figsize=(4, 3))
        fig.text(0.5, 0.5, latex_formula, fontsize=12, ha='center', va='center')

        canvas = FigureCanvasAgg(fig)
        canvas.draw()

        s, (width, height) = canvas.print_to_buffer()
        image = np.frombuffer(s, np.uint8).reshape((height, width, 4))

        image = Image.fromarray(image)
        image.save("latex.png")
    
    def start(self):
        try:
            n = int(self.entry.get())
        except ValueError:
            messagebox.showerror("Error", "Enter integer value")
            return
        
        if n <= 2:
            messagebox.showerror("Error", "Number of elements must be greater than 2")
            return
        
        window_closed = get_solution(n)
        if window_closed: self.root.destroy()
        

        
        

    