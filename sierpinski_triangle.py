import turtle as t
from random import randint
SCREEN_SIZE = 1000, 1000
t.screensize(*SCREEN_SIZE)


def color():
    # return f'#{hex(randint(0, 255))[2:].zfill(2)}{hex(randint(0, 255))[2:].zfill(2)}{hex(randint(0, 255))[2:].zfill(2)}'
    tone = (t.xcor() + SCREEN_SIZE[0]/2, t.ycor() + SCREEN_SIZE[1]/2)
    tone = (256 * tone[0]/SCREEN_SIZE[0], 256 * tone[1]/SCREEN_SIZE[1])
    # print(tone)
    return f'#{hex(int(tone[0]))[2:].zfill(2)}{hex(255)[2:].zfill(2)}{hex(int(tone[1]))[2:].zfill(2)}'


t.tracer(0)
t.up()
t.bgcolor('#333343')
screen = t.Screen()
DOTS_CONFIG = 4, color
DOTS_COUNT = int(screen.numinput('Треугольник Серпинского', 'Количество точек (4 из них будут расставлены вручную, остальные программой):', minval=1))-4
kostyl = False
already_worked = False
positions = []


def dot_on(*args):
    global kostyl, already_worked
    t.goto(*args)
    t.dot(DOTS_CONFIG[0], DOTS_CONFIG[1]())
    t.update()
    if len(positions) < 3:
        positions.append(args)
    else:
        kostyl = True
    if not already_worked:
        main()


def main():
    global kostyl, already_worked
    if kostyl:
        already_worked = True
        for _ in range(DOTS_COUNT):
            chosen_one = positions[randint(0, 2)]
            new_cords = (t.pos()[0] + chosen_one[0]) / 2, (t.pos()[1] + chosen_one[1]) / 2
            dot_on(new_cords)


screen.onclick(dot_on)
t.done()
