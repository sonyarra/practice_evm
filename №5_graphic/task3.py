import tkinter as tk
import random

def random_color():
    return f"#{random.randint(0, 0xFFFFFF):06x}"

def draw_circle(event):
    x, y = event.x, event.y
    print(f"Координаты клика: ({x}, {y})")

    r = 20 
    color = random_color()
    canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="black")

root = tk.Tk()
root.title("Рисование кругов")
root.geometry("600x400")

canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.pack()

canvas.bind("<Button-1>", draw_circle)  

root.mainloop()
