import turtle
import time


def draw_koch(n, l, t):
    if n == 0:
        t.forward(l)
        return
    nl = l / 3
    draw_koch(n - 1, nl, t)
    t.left(60)
    draw_koch(n - 1, nl, t)
    t.right(120)
    draw_koch(n - 1, nl, t)
    t.left(60)
    draw_koch(n - 1, nl, t)


def measure_and_plot_koch():
    screen = turtle.Screen()
    screen.setup(1200, 800)
    screen.tracer(0, 0)

    t_koch = turtle.Turtle()
    t_koch.hideturtle()
    t_koch.speed(0)

    t_plot = turtle.Turtle()
    t_plot.hideturtle()
    t_plot.speed(0)
    t_plot.pencolor("red")

    results = []
    max_depth = 6

    for d in range(max_depth + 1):
        t_koch.clear()
        t_koch.penup()
        t_koch.goto(-200, 200)
        t_koch.pendown()

        start = time.perf_counter()
        for _ in range(3):
            draw_koch(d, 400, t_koch)
            t_koch.right(120)
        screen.update()
        end = time.perf_counter()
        results.append((d, end - start))

    t_plot.penup()
    t_plot.goto(-500, -350)
    t_plot.pendown()
    t_plot.goto(500, -350)
    t_plot.penup()
    t_plot.goto(-500, -350)
    t_plot.pendown()
    t_plot.goto(-500, 50)

    max_time = results[-1][1]
    x_step = 800 / max_depth
    y_scale = 300 / max_time if max_time > 0 else 1

    t_plot.penup()
    t_plot.pencolor("blue")
    for d, elapsed in results:
        x = -500 + d * x_step
        y = -350 + elapsed * y_scale
        t_plot.goto(x, y)
        t_plot.dot(5)
        t_plot.pendown()

    screen.update()
    screen.exitonclick()


if __name__ == "__main__":
    measure_and_plot_koch()