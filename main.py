import importlib

for day_number in range(1, 25):
    day_module_solution = importlib.import_module(f"day{day_number}.solution")
    print(f"Day {day_number}:")
    if "solve_example" in dir(day_module_solution):
        print(f"example: {day_module_solution.solve_example()}")
    print(day_module_solution.first_puzzle_solution())
    print(day_module_solution.second_puzzle_solution())
    print("")
