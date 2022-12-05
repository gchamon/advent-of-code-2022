with open("day1/puzzle_input.txt") as input_fp:
    puzzle_input = input_fp.read()
    elves_raw = puzzle_input.split("\n\n")
    elves_split_str = (elf.split("\n") for elf in elves_raw)
    elves_food_calories = ([int(elf_food_calories_str) for elf_food_calories_str in elf]
                           for elf in elves_split_str)
    elves_calories_total = (sum(elf_food_calories)
                            for elf_food_calories in elves_food_calories)
    sorted_elves_calories = sorted(enumerate(elves_calories_total),
                                   key=lambda x: x[1],
                                   reverse=True)


def first_puzzle_solution():
    elf_with_most_calories = sorted_elves_calories[0]
    return elf_with_most_calories


def second_puzzle_solution():
    top_three_elves = sorted_elves_calories[:3]
    top_three_elves_calories = list(zip(*top_three_elves))[1]
    return sum(top_three_elves_calories)
