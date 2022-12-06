from itertools import chain, islice

letters = (chr(i)
           for i in chain(range(97, 123), range(65, 91)))
letter_priorities = {letter: index + 1
                     for index, letter in enumerate(letters)}


# this code is from a stack overflow answer
# how this works is through islice returning a slice of a iterator
# however, we can't just put the islice in a for yield because we would have no way of knowing when the
# original iterator was completely consumed
# to solve this, the first item of the slice is retrieved and then chained to the rest of the slice
# this way, the for loop breaks as soon as the there is no more item in the iterator to be retrieved
def chunks(iterable, size):
    iterator = iter(iterable)
    for first in iterator:
        yield chain([first], islice(iterator, size - 1))


def _get_compartments(input_file):
    with open(input_file) as input_fp:
        rucksacks = (line.strip() for line in input_fp.readlines())

    rucksacks_compartments = (
        (rucksack[0:(int(len(rucksack) / 2))], rucksack[(int(len(rucksack) / 2)):int(len(rucksack))])
        for rucksack in rucksacks
    )
    return rucksacks_compartments


def _get_repeated_items(rucksacks_compartments):
    compartments_intersections = (list(_intersection(set(compartment) for compartment in rucksack_compartments))
                                  for rucksack_compartments in rucksacks_compartments)
    repeated_items = (intersection[0]
                      for intersection in compartments_intersections
                      if intersection)
    return repeated_items


def _get_repeated_items_priorities(rucksacks_compartments):
    repeated_items = _get_repeated_items(rucksacks_compartments)
    repeated_items_priorities = (letter_priorities[item] for item in repeated_items)
    return repeated_items_priorities


def _get_elves_groups(input_file):
    with open(input_file) as input_fp:
        rucksacks = (line.strip() for line in input_fp.readlines())
    group_size = 3
    return chunks(rucksacks, group_size)

def _intersection(sets_iterator):
    intersection = next(sets_iterator)
    for next_set in sets_iterator:
        intersection = intersection.intersection(next_set)

    return list(intersection)

def _get_elves_groups_badges_priorities(elves_groups):
    return (letter_priorities[_intersection((set(elf_in_group) for elf_in_group in elves_group))[0]]
            for elves_group in elves_groups)


def solve_example():
    input_file = "day3/example.txt"
    rucksacks_compartments = _get_compartments(input_file)
    repeated_items_priorities = _get_repeated_items_priorities(rucksacks_compartments)
    sum_priorities = sum(repeated_items_priorities)
    return sum_priorities, sum(_get_elves_groups_badges_priorities(_get_elves_groups(input_file)))


def first_puzzle_solution():
    rucksacks_compartments = _get_compartments("day3/puzzle_input.txt")
    repeated_items_priorities = _get_repeated_items_priorities(rucksacks_compartments)
    sum_priorities = sum(repeated_items_priorities)
    return sum_priorities


def second_puzzle_solution():
    elves_groups = _get_elves_groups("day3/puzzle_input.txt")
    groups_badges_priorites = _get_elves_groups_badges_priorities(elves_groups)
    return sum(groups_badges_priorites)
