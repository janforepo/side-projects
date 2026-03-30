import random
import turtle
import time

screen = turtle.Screen()
screen.colormode(255)
screen.bgcolor("black")
screen.setup(width=1200, height=800)

t = turtle.Turtle()
t.speed(0)
t.pensize(9)

colors = ("#ff2c2c", "#fff600", "#0096ff", "#1fd655",
          "#b250f0", "#ffa500", "#ff66cc")

def random_color():
    return random.choice(colors)

for i in range(1, 300, 1): # Edit the middle number to change the amount of lines drawn.
    q = random_color()
    t.pencolor(q)
    # t.circle(i)
    # t.circle(-i) uncomment to draw circles
    t.forward(i)
    t.right(119) # Triangle 119°, square 89°, pentagon 69°, hexagon 59°.
    print(i)
    time.sleep(0)

turtle.done()
