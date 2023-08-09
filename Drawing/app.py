import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw
from predict import predict_image
import os

# Paths to different models
spiralModel = os.path.join("models", "random_forest_spiral_model.pkl")
waveModel = os.path.join("models", "random_forest_wave_model.pkl")

class ParkinsonsDetectorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Parkinson's Detector")
        self.geometry("800x600")
        
        self.setup_ui()

    def setup_ui(self):
        self.canvas = tk.Canvas(self, bg="white", width=800, height=500)
        self.canvas.pack(pady=10)
        
        self.drawing = False
        self.brushSize = 12
        self.brushColor = "black"
        self.lastPoint = None
        
        self.create_menus()
        self.create_options_bar()
        self.create_output_label()

        self.canvas.bind("<ButtonPress-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

    def create_menus(self):
        main_menu = tk.Menu(self)
        self.config(menu=main_menu)

        file_menu = tk.Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save_canvas)
        file_menu.add_command(label="Clear", command=self.clear_canvas)

        detect_menu = tk.Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="Detect", menu=detect_menu)
        detect_menu.add_command(label="Spiral", command=self.detect_spiral)
        detect_menu.add_command(label="Wave", command=self.detect_wave)

        brush_size_menu = tk.Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="Brush Size", menu=brush_size_menu)
        brush_size_menu.add_command(label="4px", command=lambda: self.set_brush_size(4))
        brush_size_menu.add_command(label="7px", command=lambda: self.set_brush_size(7))
        brush_size_menu.add_command(label="9px", command=lambda: self.set_brush_size(9))
        brush_size_menu.add_command(label="12px", command=lambda: self.set_brush_size(12))

    def create_options_bar(self):
        options_frame = tk.Frame(self)
        options_frame.pack(fill=tk.BOTH, padx=10)

        self.brush_size_label = tk.Label(options_frame, text="Brush Size:")
        self.brush_size_label.pack(side=tk.LEFT)

        self.canvas.bind("<ButtonPress-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

    def create_output_label(self):
        self.output_label = tk.Label(self, text="", font=("Arial", 25))
        self.output_label.pack(pady=10)

    def start_drawing(self, event):
        self.drawing = True
        self.lastPoint = (event.x, event.y)

    def draw(self, event):
        if self.drawing:
            x, y = event.x, event.y
            self.canvas.create_line(
                self.lastPoint[0], self.lastPoint[1], x, y,
                fill=self.brushColor, width=self.brushSize,
                capstyle=tk.ROUND, joinstyle=tk.ROUND
            )
            self.lastPoint = (x, y)

    def stop_drawing(self, event):
        self.drawing = False

    def save_canvas(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")]
        )
        if file_path:
            self.canvas.postscript(file=file_path + ".eps", colormode="color")
            img = Image.open(file_path + ".eps")
            img.save(file_path)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.output_label.config(text="")

    def detect_spiral(self):
        temp_path = "temp.png"
        self.canvas.postscript(file=temp_path + ".eps", colormode="color")
        img = Image.open(temp_path + ".eps")
        img.save(temp_path)

        pred = predict_image(temp_path, spiralModel)
        os.remove(temp_path)

        self.output_label.config(text=pred, fg="green" if pred == "Healthy" else "red")

    def detect_wave(self):
        temp_path = "temp.png"
        self.canvas.postscript(file=temp_path + ".eps", colormode="color")
        img = Image.open(temp_path + ".eps")
        img.save(temp_path)

        pred = predict_image(temp_path, waveModel)
        os.remove(temp_path)

        self.output_label.config(text=pred, fg="green" if pred == "Healthy" else "red")

    def set_brush_size(self, size):
        self.brushSize = size

if __name__ == "__main__":
    app = ParkinsonsDetectorApp()
    app.mainloop()
