import os
import re
from collections import defaultdict
from typing import List


class REPL:
    repl_stack: List[str]
    cwd: List[str]
    cur_cmd: str
    cmd_proc = re.compile(r"^\$ (?P<cmd>\w+)( )?(?P<arg>.*)?$")
    file_proc = re.compile(r"^(?P<file_size>\d+) (?P<filename>.*)$")
    dir_proc = re.compile(r"^dir (?P<dir_name>.*)$")

    def __init__(self, filename):
        self.dirs = defaultdict(lambda: {"size": 0, "files": set()})
        with open(filename) as input_fp:
            self.repl_stack = [line.strip() for line in input_fp.readlines()]

    def get_next_cmd(self):
        self.cur_cmd = self.repl_stack.pop(0)

    def process_current_command(self):
        # print(self.cur_cmd)
        cmd_match = self.cmd_proc.match(self.cur_cmd)
        if cmd_match.group("cmd") == "cd":
            self.process_cd(cmd_match.group("arg"))
        elif cmd_match.group("cmd") == "ls":
            self.process_ls()
        else:
            raise Exception(f"Unknown cmd {cmd_match.group('cmd')}")

    def process_cd(self, cd_arg):
        if cd_arg == "/":
            self.cwd = ["/"]
        elif cd_arg == "..":
            self.cwd.pop()
        else:
            self.cwd.append(cd_arg)
        # print(self.cwd)

    def process_ls(self):
        ls_output = []
        cwd_str = os.path.join(*self.cwd)
        while self.repl_stack and not self.repl_stack[0].startswith("$"):
            ls_output.append(self.repl_stack.pop(0))
        else:
            for output_line in ls_output:
                if file_match := self.file_proc.match(output_line):
                    filename = file_match.group("filename")
                    file_size = file_match.group("file_size")
                    if file_match.group("filename") not in self.dirs[cwd_str]["files"]:
                        for i in range(1, len(self.cwd) + 1):
                            # print(self.cwd[:i], file_size)
                            self.dirs[os.path.join(*self.cwd[:i])]["size"] += int(file_size)
                        self.dirs[os.path.join(*self.cwd)]["files"].add(filename)
                    # else:
                    #     print(f"file already processed: {filename}")
                # elif dir_match := self.dir_proc.match(output_line):
                #     print(dir_match.group("dir_name"))
                # else:
                #     raise Exception(f"ls line {output_line}")

    def run(self):
        while self.repl_stack:
            self.get_next_cmd()
            self.process_current_command()


def sum_dirs_dedupe(repl: REPL):
    total = 0
    summed_dirs = set()

    small_dirs = ((cur_dir, metadata) for cur_dir, metadata in puzzle_repl.dirs.items()
                  if metadata["size"] <= 100000)
    small_sorted_dirs = sorted(small_dirs, key=lambda x: x[0])

    for cur_dir, metadata in small_sorted_dirs:
        # if not any(cur_dir.startswith(cur_summed_dir) for cur_summed_dir in summed_dirs):
        total += metadata["size"]
        summed_dirs.add(cur_dir)

    return total


def solve_example():
    repl = REPL("day7/example.txt")
    repl.run()
    return sum_dirs_dedupe(repl)


puzzle_repl = REPL("day7/puzzle_input.txt")
puzzle_repl.run()


def first_puzzle_solution():
    return sum_dirs_dedupe(puzzle_repl)


def second_puzzle_solution():
    total_fs_size = 70000000
    needed_free_space = 30000000
    cur_unused = total_fs_size - puzzle_repl.dirs["/"]["size"]
    needed_to_free = needed_free_space - cur_unused
    dirs_sorted_by_size = sorted(puzzle_repl.dirs.values(), key=lambda x: x["size"])
    smallest_possible_dir = next(cur_dir for cur_dir in dirs_sorted_by_size
                                 if cur_dir["size"] >= needed_to_free)
    return smallest_possible_dir["size"]
