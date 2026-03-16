import tkinter as tk

root = tk.Tk()
root.title("Движение квадрата")
root.geometry("600x400")

canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.pack()

size = 50
x, y = 0, 175
square = canvas.create_rectangle(x, y, x + size, y + size, fill="blue")

speed = 10

def move():
    global x
    if x + size < 600: 
        x += speed
        canvas.coords(square, x, y, x + size, y + size)
        root.after(50, move) 
    else:
        print("Движение остановлено — достигнут край окна")

move()
root.mainloop()
