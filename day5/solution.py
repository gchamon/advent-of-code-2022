import re
from itertools import zip_longest


def get_puzzle_stack(lines):
    stacks = list(zip_longest(*lines[:8]))[1::4]
    stacks_sanitized = [[crate for crate in stack if crate not in {' ', None}][::-1]
                        for stack in stacks]
    return stacks_sanitized


def get_commands(lines):
    cmd_re = re.compile(r"move (\d+) from (\d+) to (\d+)")
    return [[int(c) for c in cmd_re.match(line).groups()]
            for line in lines[10:]]


def operate_over_stacks(stacks, command, must_reverse):
    amount, from_stack, to_stack = command
    from_stack -= 1
    to_stack -= 1
    stacks_to_move = stacks[from_stack][-amount:]
    stacks[to_stack] += (stacks_to_move[::-1] if must_reverse else stacks_to_move)
    stacks[from_stack] = stacks[from_stack][:len(stacks[from_stack]) - amount]


def get_stack_and_commands():
    with open("day5/puzzle_input.txt") as input_fp:
        lines = [line.strip() for line in input_fp.readlines()]
    stack = get_puzzle_stack(lines)
    commands = get_commands(lines)
    return commands, stack


def first_puzzle_solution():
    commands, stacks = get_stack_and_commands()
    for command in commands:
        operate_over_stacks(stacks, command, must_reverse=True)

    return ''.join(stack[-1] for stack in stacks)


def second_puzzle_solution():
    commands, stacks = get_stack_and_commands()
    for command in commands:
        operate_over_stacks(stacks, command, must_reverse=False)

    return ''.join(stack[-1] for stack in stacks)
