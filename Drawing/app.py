import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw
import os

# Placeholder function for image prediction
def predict_image(image_path, model_path):
    # Replace this with your actual prediction logic
    # Load the image from the path and perform the prediction using the model
    # Return the predicted label (e.g., "Healthy" or "Parkinson's")
    return "Healthy"  # Placeholder prediction

class Window(tk.Tk):
    def __init__(self):
        super().__init__()

        # setting title
        self.title("Parkinson's Detector")

        # setting geometry to main window
        self.geometry("800x600")

        # create a frame for the canvas and label
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # creating canvas
        self.canvas = tk.Canvas(self.main_frame, bg="white", width=600, height=600)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # variables
        self.drawing = False
        self.brushSize = 12
        self.brushColor = "black"
        self.lastPoint = None

        # create a frame for buttons and label
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # create a label for output predictions
        self.label = tk.Label(self.button_frame, text="", font=("Arial", 20), bg="white")
        self.label.pack(fill=tk.X, padx=10, pady=10)

        # create buttons for save and clear actions
        save_button = tk.Button(self.button_frame, text="Save", command=self.save, padx=10)
        save_button.pack(fill=tk.X, padx=10, pady=5)

        clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear, padx=10)
        clear_button.pack(fill=tk.X, padx=10, pady=5)

        # create buttons for detecting spiral and wave patterns
        detect_spiral_button = tk.Button(self.button_frame, text="Detect Spiral", command=self.detect_spiral, padx=10)
        detect_spiral_button.pack(fill=tk.X, padx=10, pady=5)

        detect_wave_button = tk.Button(self.button_frame, text="Detect Wave", command=self.detect_wave, padx=10)
        detect_wave_button.pack(fill=tk.X, padx=10, pady=5)

        # binding mouse events
        self.canvas.bind("<ButtonPress-1>", self.mouse_press)
        self.canvas.bind("<B1-Motion>", self.mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_release)

        # configure styles for buttons and labels
        self.configure_styles()

    def configure_styles(self):
        self.label.configure(relief=tk.GROOVE, bd=2)
        self.button_frame.configure(relief=tk.GROOVE, bd=2)
        self.canvas.configure(cursor="cross")

    def mouse_press(self, event):
        self.drawing = True
        self.lastPoint = (event.x, event.y)

    def mouse_move(self, event):
        if self.drawing:
            x, y = event.x, event.y
            self.canvas.create_line(self.lastPoint[0], self.lastPoint[1], x, y, fill=self.brushColor, width=self.brushSize, capstyle=tk.ROUND, joinstyle=tk.ROUND)
            self.lastPoint = (x, y)

    def mouse_release(self, event):
        self.drawing = False

    def save(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")])
        if file_path:
            self.canvas.postscript(file=file_path + ".eps", colormode="color")
            img = Image.open(file_path + ".eps")
            img.save(file_path)

    def clear(self):
        self.canvas.delete("all")
        self.label.config(text="")

    def detect_spiral(self):
        temp_path = "temp.png"
        self.canvas.postscript(file=temp_path + ".eps", colormode="color")
        img = Image.open(temp_path + ".eps")
        img.save(temp_path)

        pred = predict_image(temp_path, "path/to/spiral_model.pkl")
        # Replace "path/to/spiral_model.pkl" with the actual path to your spiral detection model
        # The predict_image function should take the image path and the model path to perform the prediction.

        self.label.config(text=pred, fg="green" if pred == "Healthy" else "red")

    def detect_wave(self):
        temp_path = "temp.png"
        self.canvas.postscript(file=temp_path + ".eps", colormode="color")
        img = Image.open(temp_path + ".eps")
        img.save(temp_path)

        pred = predict_image(temp_path, "path/to/wave_model.pkl")
        # Replace "path/to/wave_model.pkl" with the actual path to your wave detection model
        # The predict_image function should take the image path and the model path to perform the prediction.

        self.label.config(text=pred, fg="green" if pred == "Healthy" else "red")


if __name__ == "__main__":
    window = Window()
    window.mainloop()
    
    
# import tkinter as tk
# from tkinter import filedialog
# from PIL import Image, ImageDraw
# from predict import predict_image
# import os

# # paths to different models
# spiralModel = os.path.join("models", "random_forest_spiral_model.pkl")
# waveModel = os.path.join("models", "random_forest_wave_model.pkl")


# class Window(tk.Tk):
#     def __init__(self):
#         super().__init__()

#         # setting title
#         self.title("Parkinson's Detector")

#         # setting geometry to main window
#         self.geometry("800x600")

#         # creating canvas
#         self.canvas = tk.Canvas(self, bg="white", width=800, height=600)
#         self.canvas.pack()

#         # variables
#         self.drawing = False
#         self.brushSize = 12
#         self.brushColor = "black"
#         self.lastPoint = None

#         # create menu bar
#         mainMenu = tk.Menu(self)
#         self.config(menu=mainMenu)

#         # create file menu for save and clear action
#         fileMenu = tk.Menu(mainMenu, tearoff=0)
#         mainMenu.add_cascade(label="File", menu=fileMenu)
#         fileMenu.add_command(label="Save", command=self.save)
#         fileMenu.add_command(label="Clear", command=self.clear)

#         # create detect menu for spiral and wave detection
#         detectMenu = tk.Menu(mainMenu, tearoff=0)
#         mainMenu.add_cascade(label="Detect", menu=detectMenu)
#         detectMenu.add_command(label="Spiral", command=self.detect_spiral)
#         detectMenu.add_command(label="Wave", command=self.detect_wave)

#         # options for output label
#         self.label = tk.Label(self, text="", font=("Arial", 25))
#         self.label.place(relx=0.5, rely=0.9, anchor="center")

#         # create options for brush sizes
#         brushSizeMenu = tk.Menu(mainMenu, tearoff=0)
#         mainMenu.add_cascade(label="Brush Size", menu=brushSizeMenu)
#         brushSizeMenu.add_command(label="4px", command=lambda: self.set_brush_size(4))
#         brushSizeMenu.add_command(label="7px", command=lambda: self.set_brush_size(7))
#         brushSizeMenu.add_command(label="9px", command=lambda: self.set_brush_size(9))
#         brushSizeMenu.add_command(label="12px", command=lambda: self.set_brush_size(12))

#         # binding mouse events
#         self.canvas.bind("<ButtonPress-1>", self.mouse_press)
#         self.canvas.bind("<B1-Motion>", self.mouse_move)
#         self.canvas.bind("<ButtonRelease-1>", self.mouse_release)

#     def mouse_press(self, event):
#         self.drawing = True
#         self.lastPoint = (event.x, event.y)

#     def mouse_move(self, event):
#         if self.drawing:
#             x, y = event.x, event.y
#             self.canvas.create_line(self.lastPoint[0], self.lastPoint[1], x, y, fill=self.brushColor, width=self.brushSize, capstyle=tk.ROUND, joinstyle=tk.ROUND)
#             self.lastPoint = (x, y)

#     def mouse_release(self, event):
#         self.drawing = False

#     def save(self):
#         file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")])
#         if file_path:
#             self.canvas.postscript(file=file_path + ".eps", colormode="color")
#             img = Image.open(file_path + ".eps")
#             img.save(file_path)

#     def clear(self):
#         self.canvas.delete("all")
#         self.label.config(text="")

#     def detect_spiral(self):
#         temp_path = "temp.png"
#         self.canvas.postscript(file=temp_path + ".eps", colormode="color")
#         img = Image.open(temp_path + ".eps")
#         img.save(temp_path)

#         pred = predict_image(temp_path, spiralModel)
#         os.remove(temp_path)

#         self.label.config(text=pred, fg="green" if pred == "Healthy" else "red")

#     def detect_wave(self):
#         temp_path = "temp.png"
#         self.canvas.postscript(file=temp_path + ".eps", colormode="color")
#         img = Image.open(temp_path + ".eps")
#         img.save(temp_path)

#         pred = predict_image(temp_path, waveModel)
#         os.remove(temp_path)

#         self.label.config(text=pred, fg="green" if pred == "Healthy" else "red")

#     def set_brush_size(self, size):
#         self.brushSize = size


# if __name__ == "__main__":
#     window = Window()
#     window.mainloop()

