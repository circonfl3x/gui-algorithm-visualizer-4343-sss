from dokusan import generators, solvers
from pprint import pprint
import numpy as np

def generate_puzzle():
    field = generators.random_sudoku(avg_rank=100)
    field_np = np.array(list(str(field)), dtype=int).reshape(9, 9)

    return field, field_np

def get_solution(field):
    solution = solvers.backtrack(field)
    solution_np = np.array(list(str(solution)), dtype=int).reshape(9, 9)

    return solution, solution_np