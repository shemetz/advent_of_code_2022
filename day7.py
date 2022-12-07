import dataclasses
from typing import List


@dataclasses.dataclass
class Thing:
    name: str
    pass


@dataclasses.dataclass
class File(Thing):
    size: int


@dataclasses.dataclass
class Directory(Thing):
    contents: List[Thing]

    def calc_size(self) -> int:
        total: int = 0
        for x in self.contents:
            if isinstance(x, File):
                total += x.size
            else:
                x: Directory
                total += x.calc_size()
        return total


with open('day7.txt') as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

top_level_directory = Directory(name='/', contents=[])
current_path: List[Directory] = [top_level_directory]  # index -1 is current directory

for line in input_lines:
    current_directory = current_path[-1]
    if line.startswith('$ cd /'):
        current_path[-1] = top_level_directory
    elif line.startswith('$ cd ..'):
        current_path.pop()
    elif line.startswith('$ cd '):  # (+name)
        inner_dir = line[len('$ cd '):]
        subdirectory = next(d for d in current_directory.contents if d.name == inner_dir and isinstance(d, Directory))
        current_path.append(subdirectory)
    elif line.startswith('$ ls'):
        # will add next lines as subcontents
        # handled in the following "else" branch
        pass
    else:  # line does not start with $ at all, and is in fact just one of the `ls` outputs
        part_1, part_2 = line.split(' ')
        if part_1 == 'dir':
            new_directory = Directory(name=part_2, contents=[])
            current_directory.contents.append(new_directory)
        else:
            new_file = File(name=part_2, size=int(part_1))
            current_directory.contents.append(new_file)


THRESHOLD = 100000


def calculate_sum_recursively(dir: Directory):
    sum_of_smallest_dirs = 0
    dir_size = dir.calc_size()
    if dir_size <= THRESHOLD:
        sum_of_smallest_dirs += dir_size
    for subdir in dir.contents:
        if isinstance(subdir, Directory):
            sum_of_smallest_dirs += calculate_sum_recursively(subdir)
            # possibly optimization:  avoid checking threshold for subdirs, just add all of them, if this one passes
    return sum_of_smallest_dirs


print(calculate_sum_recursively(top_level_directory))  # 1845346

TOTAL_SIZE_OF_FILESYSTEM = 70000000
SIZE_REQUIRED_FOR_UPDATE = 30000000
total_size_currently_available = TOTAL_SIZE_OF_FILESYSTEM - top_level_directory.calc_size()
need_to_empty = SIZE_REQUIRED_FOR_UPDATE - total_size_currently_available


def calculate_minimum_size_necessary_recursively(dir: Directory):
    best_of_inner_dirs = 99999999
    dir_size = dir.calc_size()
    if dir_size >= need_to_empty:
        best_of_inner_dirs = dir_size
    for subdir in dir.contents:
        if isinstance(subdir, Directory):
            best_of_inner_dirs = min(calculate_minimum_size_necessary_recursively(subdir), best_of_inner_dirs)
    return best_of_inner_dirs


print(calculate_minimum_size_necessary_recursively(top_level_directory))  # 3636703
