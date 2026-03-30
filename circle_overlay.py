from tkinter import *
import tkinter as tk
from random import *

# main window
window = Tk()
window.title("Dynamic Circle Generator")

# Initial size
canvas_width = 500
canvas_height = 500

# input frame for label + entry
input_frame = tk.Frame(window)
# We use 'fill=X' so the top bar stays at the top but spans the width
input_frame.pack(side=TOP, fill=X, pady=10)

# drawing area
# 'expand=True' and 'fill=BOTH' allow the canvas to grow with the window
field = Canvas(window, width=canvas_width, height=canvas_height, bg="white")
field.pack(expand=True, fill=BOTH)

# counter box
counter = Text(window, width=25, height=1)
counter.pack(side=BOTTOM, pady=5)

x = 0  # start at zero
running = False  # control flag

# create label and entry for speed input
speed_label = tk.Label(input_frame, text="Speed (ms):")
speed_label.grid(row=0, column=0, padx=5)

speed_entry = tk.Entry(input_frame, width=10)
speed_entry.insert(0, "100")
speed_entry.grid(row=0, column=1, padx=5)


def update_size(event):
    """Updates the global width and height variables when the window is resized."""
    global canvas_width, canvas_height
    canvas_width = event.width
    canvas_height = event.height


# Bind the 'Configure' event (resizing) to our update function
field.bind("<Configure>", update_size)


def draw_circle():
    global x, running

    if not running:
        return

    try:
        delay = int(speed_entry.get())
    except ValueError:
        delay = 100

    # Draw random circle using the updated width/height
    color = choice(["#00B4D8", "#00BF00", "#FFDE21", "#FF0000", "#FFA500", "#FD3DB5"])

    # Calculate random positions based on CURRENT canvas size
    x0 = randint(0, canvas_width)
    y0 = randint(0, canvas_height)
    diameter = randint(10, int(min(canvas_width, canvas_height) / 5))

    field.create_oval(x0, y0, x0 + diameter, y0 + diameter, fill=color, outline="black")

    x += 1
    counter.delete("1.0", END)
    counter.insert(END, f"Circles drawn: {x}")

    window.after(delay, draw_circle)


def start():
    global running
    if not running:
        running = True
        draw_circle()


def stop():
    global running
    running = False


# buttons to control generation
start_button = tk.Button(input_frame, text="Start", command=start)
start_button.grid(row=0, column=2, padx=5)

stop_button = tk.Button(input_frame, text="Stop", command=stop)
stop_button.grid(row=0, column=3, padx=5)

window.mainloop()