from PIL import Image
import json

wheel_dict = {
    1: (10, 20, 30, 60),
    2: (50, 20, 30, 60),
    3: (120, 20, 30, 60),
    4: (160, 20, 30, 60),

    5: (10, 90, 30, 60),
    6: (50, 90, 30, 60),
    7: (120, 90, 30, 60),
    8: (160, 90, 30, 60),

    9: (10, 160, 30, 60),
    10: (50, 160, 30, 60),
    11: (120, 160, 30, 60),
    12: (160, 160, 30, 60),

    13: (10, 230, 30, 60),
    14: (50, 230, 30, 60),
    15: (120, 230, 30, 60),
    16: (160, 230, 30, 60),

    17: (10, 300, 30, 60),
    18: (50, 300, 30, 60),
    19: (120, 300, 30, 60),
    20: (160, 300, 30, 60),

    21: (10, 370, 30, 60),
    22: (50, 370, 30, 60),
    23: (120, 370, 30, 60),
    24: (160, 370, 30, 60)
}


def add_gradient_square(canvas, start_x, start_y, width, height):
    # Создаем вертикальный градиент
    gradient = Image.new("RGB", (width, height))
    start_color = (67, 197, 226)  # #43C5E2
    end_color = (90, 92, 168)  # #5A5CA8
    for y in range(height):
        r = start_color[0] * (1 - y / height) + end_color[0] * (y / height)
        g = start_color[1] * (1 - y / height) + end_color[1] * (y / height)
        b = start_color[2] * (1 - y / height) + end_color[2] * (y / height)
        for x in range(width):
            gradient.putpixel((x, y), (int(r), int(g), int(b)))

    # Вставляем градиентный квадрат на холст
    canvas.paste(gradient, (start_x, start_y))

    return canvas


def get_result():
    with open('data/Wheels.json', 'r', encoding='utf-8') as file:
        wheels = json.load(file)

    num_axes = wheels[-1]['count']

    # Создаем пустой холст 200x300 чёрного цвета
    canvas = Image.new("RGB", (200, 70 * num_axes + 40), "black")

    # Добавляем градиентные квадраты на холст

    if len(wheels) != 0:
        for i in wheels[-1].keys():
            if 'wheel_' in i:
                canvas = add_gradient_square(canvas, *wheel_dict[int(i.replace('wheel_', ''))])

    # Сохраняем изображение
    canvas.save("canvas_with_gradient_squares.png")

# Отображаем изображение (опционально)
# canvas.show()
