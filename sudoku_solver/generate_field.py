from dokusan import generators, solvers
from pprint import pprint
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import time

def generate_puzzle():
    field = generators.random_sudoku(avg_rank=100)
    field_np = np.array(list(str(field)), dtype=int).reshape(9, 9)

    return field, field_np

def get_solution(field):
    solution = solvers.backtrack(field)
    solution_np = np.array(list(str(solution)), dtype=int).reshape(9, 9)

    return solution, solution_np

def field_to_img(field_np, cell_size=60, line_color = 'black', text_color='black', bg='white'): # 0.114502... - Время выполнения
    width = height = cell_size * 9
    img = Image.new('RGB', (width,height), color=bg)
    draw = ImageDraw.Draw(img)
    # TODO: добавить какой нибудь красивее font
    font = ImageFont.load_default(size=cell_size//2)
    #Grid lines

    for i in range(10):
        line_width = 4 if i % 3 == 0 else 1 # TODO: на каждой 3-й границей рисовать жирнее линию чтоб
                        # он будет похоже на настояшую доску судоку
        pos = i * cell_size

        draw.line([(pos, 0), (pos, height)], fill=line_color, width=line_width)
        draw.line([(0, pos), (width, pos)], fill=line_color, width=line_width)

    # Numbers
    for i in range(10):
        for rows in range(9):
            for cols in range(9):
                val = field_np[rows, cols]
                if val != 0:
                    # TODO: Убирать magic numbers и считать правильный позицию изпользуя bbox вроде
                    x = (cols*cell_size) + (cell_size // 2) - 10
                    y = (rows*cell_size) - (cell_size) + 10

                    draw.text((x,y), str(val), fill=text_color, font=font)
    return img


field = generate_puzzle() 

print(field[0])
img = field_to_img(field[1])
#img.show()
img.save("puzzle.png")
