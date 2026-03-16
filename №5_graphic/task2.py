import tkinter as tk

root = tk.Tk()
root.title("Прямоугольник и круг")
root.geometry("600x400")

canvas = tk.Canvas(root, width=400, height=300)
canvas.pack()

canvas.create_rectangle(50, 50, 150, 150, fill="red", outline="blue", width=3)

canvas.create_oval(200, 50, 300, 150, fill="yellow", outline="green", width=3)

root.mainloop()
