def get_elf_pairs_ranges(input_file):
    with open(input_file) as input_fp:
        lines = (line.strip() for line in input_fp.readlines())

    def split_range(_range):
        return [int(r) for r in _range.split("-")]

    elves_pairs = (line.split(",") for line in lines)
    elves_pairs_ranges = ((split_range(pair[0]), split_range(pair[1]))
                          for pair in elves_pairs)
    return elves_pairs_ranges


def _solve_input_first_puzzle(input_file):
    elves_pairs_ranges = get_elf_pairs_ranges(input_file)

    def range_fully_overlaps(range_a, range_b):
        return range_a[0] >= range_b[0] and range_a[1] <= range_b[1]

    fully_overlaps = (
        range_fully_overlaps(elf_range_a, elf_range_b) or range_fully_overlaps(elf_range_b, elf_range_a)
        for elf_range_a, elf_range_b in elves_pairs_ranges
    )
    return sum(fully_overlaps)


def _solve_input_second_puzzle(input_file):
    elves_pairs_ranges = get_elf_pairs_ranges(input_file)

    def range_overlaps_at_all(range_a, range_b):
        return not (range_a[1] < range_b[0] or range_a[0] > range_b[1])

    fully_overlaps = (
        range_overlaps_at_all(elf_range_a, elf_range_b)
        for elf_range_a, elf_range_b in elves_pairs_ranges
    )
    return sum(fully_overlaps)


def solve_example():
    return _solve_input_first_puzzle("day4/example.txt")


def first_puzzle_solution():
    return _solve_input_first_puzzle("day4/puzzle_input.txt")


def second_puzzle_solution():
    return _solve_input_second_puzzle("day4/puzzle_input.txt")
