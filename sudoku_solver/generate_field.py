from dokusan import generators, solvers
from pprint import pprint
import numpy as np

field = generators.random_sudoku(avg_rank=100)
field_np = np.array(list(str(field)), dtype=int).reshape(9, 9)

solution = solvers.backtrack(field)
solution_np = np.array(list(str(solution)), dtype=int).reshape(9, 9)

pprint(field_np)
pprint(solution_np)