import tkinter as tk
from random import randint
from time import time
from math import sqrt

# ---- GAME PARAMETERS ----
skore = 0
ship_r = 25
ship_speed = 10
field_height = 500
field_width = 800
mid_x = field_width / 2
mid_y = field_height / 2
window = tk.Tk()
window.title("Bubble Pop")

# ---- INPUT FRAME ----
input_frame = tk.Frame(window)
input_frame.pack(pady=10)

# ---- CANVAS ----
c = tk.Canvas(window, width=field_width, height=field_height, bg="#00B4D8")
c.pack()

# ---- SHIP ----
ship_id1 = c.create_polygon(400, 223, 380, 263, 420, 263, fill="black")
ship_id2 = c.create_polygon(400, 277, 380, 237, 420, 237, fill="black")
center_circle = c.create_oval(375, 225, 425, 275, outline="black", width=5)

# ---- BUBBLE DATA ----
bub_id = []
bub_speed = []
bub_r = []
min_bub_R = 5
max_bub_R = 20
max_bub_speed = 15
gap = 100
bub_chance = 10  # lower = more frequent
timelimit = 30
bonus_skore = 1000
bonus = 0
end = time() + timelimit

# ---- MOUSE FOLLOW SETTINGS ----
target_x, target_y = mid_x, mid_y
follow_speed = 7  # pixels per frame; smaller = slower glide

# ---- HELPER FUNCTIONS ----
def create_bub():
    x = field_width + gap
    y = randint(0, field_height)
    r = randint(min_bub_R, max_bub_R)
    id1 = c.create_oval(x - r, y - r, x + r, y + r, outline="white")
    bub_id.append(id1)
    bub_r.append(r)
    bub_speed.append(randint(1, max_bub_speed))

def get_coordenates(id_number):
    place = c.coords(id_number)
    if len(place) >= 4:
        x = (place[0] + place[2]) / 2
        y = (place[1] + place[3]) / 2
        return x, y
    return 0, 0

def distance(id1, id2):
    x1, y1 = get_coordenates(id1)
    x2, y2 = get_coordenates(id2)
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def del_bub(i):
    del bub_r[i]
    del bub_speed[i]
    c.delete(bub_id[i])
    del bub_id[i]

def clear_bub():
    for i in range(len(bub_id) - 1, -1, -1):
        x, y = get_coordenates(bub_id[i])
        if x < -gap:
            del_bub(i)

def move_bub():
    for i in range(len(bub_id)):
        c.move(bub_id[i], -bub_speed[i], 0)

def collision():
    points = 0
    for bub in range(len(bub_id) - 1, -1, -1):
        if distance(center_circle, bub_id[bub]) < (ship_r + bub_r[bub]):
            points += (bub_r[bub] + bub_speed[bub])
            del_bub(bub)
    return points

# ---- TOP UI (TIME, COORDS, SCORE) ----
time_label = tk.Label(input_frame, text=f"Time: {timelimit}", font=("Helvetica", 10, "bold"))
time_label.grid(row=0, column=0, padx=20)

ship_x_label = tk.Label(input_frame, text="x:")
ship_x_label.grid(row=0, column=1, padx=5)
ship_x_entry = tk.Entry(input_frame, width=10)
ship_x_entry.grid(row=0, column=2)

ship_y_label = tk.Label(input_frame, text="y:")
ship_y_label.grid(row=0, column=3, padx=5)
ship_y_entry = tk.Entry(input_frame, width=10)
ship_y_entry.grid(row=0, column=4)

score_label = tk.Label(input_frame, text="Score: 0", font=("Helvetica", 10, "bold"))
score_label.grid(row=0, column=5, padx=20)

ship_coordenates_x, ship_coordenates_y = get_coordenates(center_circle)
ship_x_entry.insert(0, str(int(ship_coordenates_x)))
ship_y_entry.insert(0, str(int(ship_coordenates_y)))

# ---- SHIP MOVEMENT KEYS ----
def ship_movement(event):
    global ship_coordenates_x, ship_coordenates_y
    dx, dy = 0, 0
    if event.keysym == "Up":
        dy = -ship_speed
    elif event.keysym == "Down":
        dy = ship_speed
    elif event.keysym == "Left":
        dx = -ship_speed
    elif event.keysym == "Right":
        dx = ship_speed
    if dx == dy == 0:
        return

    cur_x, cur_y = get_coordenates(center_circle)
    new_x = max(ship_r, min(field_width - ship_r, cur_x + dx))
    new_y = max(ship_r, min(field_height - ship_r, cur_y + dy))
    dx = new_x - cur_x
    dy = new_y - cur_y
    c.move(ship_id1, dx, dy)
    c.move(ship_id2, dx, dy)
    c.move(center_circle, dx, dy)
    ship_coordenates_x += dx
    ship_coordenates_y += dy

c.bind_all("<Key>", ship_movement)

# ---- MOUSE FOLLOW SYSTEM ----
def follow_mouse(event):
    global target_x, target_y
    target_x = event.x
    target_y = event.y

c.bind("<Motion>", follow_mouse)

def move_ship_toward_target():
    global ship_coordenates_x, ship_coordenates_y
    cur_x, cur_y = get_coordenates(center_circle)
    dx = target_x - cur_x
    dy = target_y - cur_y
    dist = sqrt(dx**2 + dy**2)
    if dist < follow_speed:
        return
    dx = (dx / dist) * follow_speed
    dy = (dy / dist) * follow_speed
    c.move(ship_id1, dx, dy)
    c.move(ship_id2, dx, dy)
    c.move(center_circle, dx, dy)
    ship_coordenates_x += dx
    ship_coordenates_y += dy
    ship_x_entry.delete(0, tk.END)
    ship_x_entry.insert(0, str(int(ship_coordenates_x)))
    ship_y_entry.delete(0, tk.END)
    ship_y_entry.insert(0, str(int(ship_coordenates_y)))

# ---- HUD / GAME OVER TEXT ----
game_over_text = c.create_text(mid_x, mid_y, text="", fill="white", font=("Helvetica", 30))
final_score_text = c.create_text(mid_x, mid_y + 30, text="", fill="white")

def show_skore(s):
    score_label.config(text=f"Score: {s}")

def show_time(time_left):
    # Updates the top bar UI label instead of canvas
    time_label.config(text=f"Time: {int(time_left)}")

# ---- MAIN GAME LOOP ----
def game_loop():
    global skore, bonus, end

    # move ship smoothly toward mouse
    move_ship_toward_target()

    # bubble spawning & updates
    if randint(1, bub_chance) == 1:
        create_bub()
    move_bub()
    clear_bub()
    skore += collision()

    # bonus logic
    if int(skore / bonus_skore) > bonus:
        bonus += 1
        end += timelimit

    show_skore(skore)
    show_time(max(0, end - time()))

    if time() < end:
        window.after(10, game_loop)
    else:
        c.itemconfig(game_over_text, text="GAME OVER")
        c.itemconfig(final_score_text, text=f"Score: {skore}  Bonus time: {bonus * timelimit}s")

# ---- START GAME ----
game_loop()
window.mainloop()