import turtle as t
from random import randint


def rgb_to_hex(r, g, b):
    return f'#{hex(r)[2:].zfill(2)}{hex(g)[2:].zfill(2)}{hex(b)[2:].zfill(2)}'


CELL_SIZE = 100
ITEMS_SIZE = CELL_SIZE * 0.4
FIELD_SIZE = 3
VIRTUAL_FIELD = [['_' for _ in range(FIELD_SIZE)] for _ in range(FIELD_SIZE)]
RED, GREEN, BLUE = randint(80, 160), randint(130, 255), randint(110, 220)
t.tracer(0)
t.up()
t.lt(90)
t.bgcolor(rgb_to_hex(RED, GREEN, BLUE))
t.pencolor(rgb_to_hex(255-RED, 255-GREEN, 255-BLUE))
t.pensize(2)
t.hideturtle()


def draw_cell(size, cords, inner_text=''):
    t.goto(*cords)
    t.down()
    for _ in range(4):
        t.fd(size)
        t.rt(90)
    t.up()
    t.goto(t.xcor()+CELL_SIZE//2, t.ycor()+CELL_SIZE//2)
    t.write(inner_text, align='center')


def create_field():
    field = [[0 for _ in range(FIELD_SIZE)] for _ in range(FIELD_SIZE)]
    for i in range(FIELD_SIZE):
        for j in range(FIELD_SIZE):
            draw_cell(CELL_SIZE, (CELL_SIZE*i, CELL_SIZE*j), inner_text=f'{FIELD_SIZE-1-j} {i}')
            field[i][j] = [j * CELL_SIZE, (FIELD_SIZE-1-i) * CELL_SIZE]
    return field


def draw_item(item, cords, size=ITEMS_SIZE):
    t.goto(cords[0] + CELL_SIZE//2, cords[1] + CELL_SIZE//2)
    if item in ('o', '0', 0):
        t.goto(t.xcor()+size, t.ycor())
        t.down()
        t.circle(size)
        t.up()
    else:
        size *= 0.75
        t.goto(cords[0] + CELL_SIZE//2 - size, cords[1] + CELL_SIZE//2 - size)
        t.down()
        t.goto(cords[0] + CELL_SIZE//2 + size, cords[1] + CELL_SIZE//2 + size)
        t.up()
        t.goto(cords[0] + CELL_SIZE//2 - size, cords[1] + CELL_SIZE//2 + size)
        t.down()
        t.goto(cords[0] + CELL_SIZE//2 + size, cords[1] + CELL_SIZE//2 - size)
        t.up()


def check_row(to_check):
    if not isinstance(to_check, set):
        to_check = set(to_check)
    if len(to_check) == 1 and tuple(to_check)[0] != '_':
        return tuple(to_check)[0]


def check_field(to_check):
    # Проверка главной диагонали
    main_axis = set()
    for i in range(len(to_check)):
        main_axis.add(to_check[i][i])
    if check_row(main_axis) is not None:
        return check_row(main_axis)
    # Проверка побочной диагонали
    side_axis = set()
    for j in range(len(to_check)):
        side_axis.add(to_check[j][len(to_check)-1-j])
    if check_row(side_axis) is not None:
        return check_row(side_axis)
    # Проверка горизонталей
    for row in to_check:
        if check_row(row) is not None:
            return check_row(row)
    # Проверка вертикалей
    to_check = list(zip(*to_check))
    for row in to_check:
        if check_row(row) is not None:
            return check_row(row)
    return None


field_cords = create_field()
t.update()
for move in range(FIELD_SIZE**2):
    while True:
        user_input = t.textinput('X' if move % 2 == 0 else 'O', 'Введите корректный номер клетки')
        usr_i, usr_j = [int(i) for i in user_input.split()]
        if 0 <= usr_i <= FIELD_SIZE-1 and 0 <= usr_j <= FIELD_SIZE-1 and VIRTUAL_FIELD[usr_i][usr_j] == '_':
            break
    VIRTUAL_FIELD[usr_i][usr_j] = 'x' if move % 2 == 0 else 'o'
    user_cords = field_cords[usr_i][usr_j]
    game_result = check_field(VIRTUAL_FIELD)
    draw_item('x' if move % 2 == 0 else 'o', cords=user_cords)
    t.update()
    if game_result is not None:
        print(f'{game_result.upper()} is winner!')
        break
else:
    print('Draw!')

t.exitonclick()
