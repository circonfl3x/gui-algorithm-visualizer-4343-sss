from dokusan import generators, solvers
from pprint import pprint
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from os import sys

def generate_puzzle(complexity):
    field = generators.random_sudoku(avg_rank=complexity)
    field_np = np.array(list(str(field)), dtype=int).reshape(9, 9)

    return field, field_np

def get_solution(field):
    solution = solvers.backtrack(field)
    solution_np = np.array(list(str(solution)), dtype=int).reshape(9, 9)

    return solution, solution_np

def field_from_input():
    field = []
    line_num = 0
    for line in sys.stdin:
        line_num += 1
        if line_num > 9:
            break
        line = line.strip()
        if not line:
            continue
        row = [int(x) for x in line.split()]
        if(len(row) != 9):
            raise ValueError("Row should be 9 digits long")
        for i in row:
            if i < 0 or i>9:
                raise ValueError(f"Element on position {i+1}, line {line_num+1} is out of range")
        field.append(row)
    return field
    
def field_from_file(uploaded_file):
    field = []

    if uploaded_file is None:
        raise ValueError("Файл не выбран")

    try:
        content = uploaded_file.getvalue().decode("utf-8-sig")
    except UnicodeDecodeError:
        raise ValueError("Файл должен быть текстовым в кодировке UTF-8")

    for line_num, line in enumerate(content.splitlines(), start=1):
        line = line.strip()

        if not line:
            continue

        if len(field) >= 9:
            raise ValueError("В файле должно быть ровно 9 непустых строк")

        try:
            row = [int(value) for value in line.split()]
        except ValueError:
            raise ValueError(
                f"Строка {line_num} содержит нецелое значение"
            )

        if len(row) != 9:
            raise ValueError(
                f"В строке {line_num} должно быть ровно 9 чисел"
            )

        for column_num, value in enumerate(row, start=1):
            if not 0 <= value <= 9:
                raise ValueError(
                    f"Значение в строке {line_num}, "
                    f"столбце {column_num} должно быть от 0 до 9"
                )

        field.append(row)

    if len(field) != 9:
        raise ValueError(
            f"В файле должно быть 9 непустых строк, получено: {len(field)}"
        )

    return field

def field_to_img(
        field_np,
        cell_size=60,
        line_color = 'white',
        text_color='white',
        generated_text_color='red',
        bg='black',
        fixed_cells=None):
    field_np = np.array(field_np)
    width = height = cell_size * 9
    img = Image.new('RGB', (width,height), color=bg)
    draw = ImageDraw.Draw(img)
    # TODO: добавить какой нибудь красивее font
    font = ImageFont.load_default(size=cell_size//2)
    #Grid lines

    for i in range(10):
        line_width = 4 if i % 3 == 0 else 1
        pos = i * cell_size

        draw.line([(pos, 0), (pos, height)], fill=line_color, width=line_width)
        draw.line([(0, pos), (width, pos)], fill=line_color, width=line_width)

# Numbers
    fixed_cells = fixed_cells or set()
    for row in range(9):
        for col in range(9):
            val = field_np[row, col]
            if val != 0:
                text = str(val)

                bbox = draw.textbbox((0,0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                x = col * cell_size + (cell_size - text_width) / 2
                y = row * cell_size + (cell_size - text_height) / 2 - 2

                color = text_color if (row, col) in fixed_cells else generated_text_color
                draw.text((x, y), text, fill=color, font=font)
    return img
