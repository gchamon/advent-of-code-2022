def get_signals(filename):
    with open(filename) as input_fp:
        return [line.strip() for line in input_fp]


def stream_chunks(signal, marker_len):
    for i in range(0, len(signal) - marker_len + 1):
        yield signal[i:i + marker_len]


def get_marker_and_index(signal_stream, marker_len):
    chunk_sets = ((index, set(chunk)) for index, chunk in enumerate(signal_stream))
    marker = next((index, chunk_set)
                  for index, chunk_set in chunk_sets
                  if len(chunk_set) == marker_len)
    return marker


def solve_puzzle(filename, marker_len):
    signal_streams = (stream_chunks(signal, marker_len) for signal in get_signals(filename))
    markers = (get_marker_and_index(ss, marker_len) for ss in signal_streams)
    start_of_packets = (index + marker_len for index, _ in markers)
    return list(start_of_packets)


def solve_example():
    filename = "day6/example.txt"
    start_of_packet_len = 4
    return solve_puzzle(filename, start_of_packet_len)


def first_puzzle_solution():
    filename = "day6/puzzle_input.txt"
    start_of_packet_len = 4
    return solve_puzzle(filename, start_of_packet_len)[0]


def second_puzzle_solution():
    filename = "day6/puzzle_input.txt"
    start_of_message_len = 14
    return solve_puzzle(filename, start_of_message_len)[0]
