import tkinter as tk

root = tk.Tk()
root.title("Управление объектом стрелками")
width, height = 600, 400
root.geometry(f"{width}x{height}")

canvas = tk.Canvas(root, width=width, height=height, bg="white")
canvas.pack()

r = 20
x, y = width // 2, height // 2
circle = canvas.create_oval(x - r, y - r, x + r, y + r, fill="pink")

step = 10 

def move_circle(event):
    nonlocal_x, nonlocal_y = canvas.coords(circle)[0], canvas.coords(circle)[1]
    left, top, right, bottom = canvas.coords(circle)
    dx, dy = 0, 0

    if event.keysym == "Left":
        if left - step >= 0:
            dx = -step
    elif event.keysym == "Right":
        if right + step <= width:
            dx = step
    elif event.keysym == "Up":
        if top - step >= 0:
            dy = -step
    elif event.keysym == "Down":
        if bottom + step <= height:
            dy = step

    if dx != 0 or dy != 0:
        canvas.move(circle, dx, dy)

root.bind("<Key>", move_circle)
root.mainloop()
