import generate_field as gf


if __name__ == "__main__":
    field, field_np = gf.generate_puzzle()
    solution, solution_np = gf.get_solution(field)

    print("Generated Sudoku Puzzle:")
    print(field_np)
    print("\nSolution:")
    print(solution_np)