opponent_keys = ("A", "B", "C")
my_keys = ("X", "Y", "Z")

key_ranks = {key: index + 1 for index, key in enumerate(opponent_keys)}

loses_over = {key: opponent_keys[(index + 1) % len(opponent_keys)] for index, key in enumerate(opponent_keys)}
wins_over = dict(list(zip(loses_over.values(), loses_over.keys())))


def const(y):
    return lambda x: y


decryption_key_first_puzzle = {my_key: const(opponent_key)
                               for my_key, opponent_key in zip(my_keys, opponent_keys)}

decryption_key_second_puzzle = {
    "X": lambda opk: wins_over[opk],
    "Y": lambda opk: opk,
    "Z": lambda opk: loses_over[opk]
}


def _rank_round(opponent_key, my_key):
    key_rank = key_ranks[my_key]
    if my_key == opponent_key:
        outcome = 3
    else:
        outcome = (0 if loses_over[my_key] == opponent_key else 6)

    return key_rank + outcome


def _solve_puzzle(input_file, decryption_key):
    with open(input_file) as input_fp:
        rounds = (line.strip().split(" ") for line in input_fp.readlines())
    rounds_decrypted = ((cur_round[0], decryption_key[cur_round[1]](cur_round[0]))
                        for cur_round in rounds)
    rounds_ranked = (_rank_round(cur_round[0], cur_round[1])
                     for cur_round in rounds_decrypted)
    total_score = sum(rounds_ranked)
    print(total_score)


def solve_example():
    _solve_puzzle("day2/example.txt", decryption_key_first_puzzle)


def first_puzzle_solution():
    _solve_puzzle("day2/puzzle_input.txt", decryption_key_first_puzzle)


def second_puzzle_solution():
    _solve_puzzle("day2/puzzle_input.txt", decryption_key_second_puzzle)
