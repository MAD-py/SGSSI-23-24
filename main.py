import sys
import re

from os import listdir, path
from hashlib import sha256
from typing import Iterator


def check_prefix_sha256(candidate_file_name: str) -> tuple[bool, int]:
    with open(candidate_file_name, "rb") as f:
        text = f.read()
    
    sha_256 = sha256(text).hexdigest()
    zeros_number = re.search("^0{2,}", sha_256)

    if zeros_number:
        return True, len(zeros_number.group())
    return False, 0


def check_file_structure(identifier: str, candidate_file_name: str, file_name: str) -> bool:
    with open(file_name, "r") as f:
        file = f.read()

    with open(candidate_file_name, "r") as f:
        candidate = f.read()

    if not candidate.startswith(file):
        return False
    
    candidate_last_line = candidate.replace(file, "")
    return bool(re.search(rf"^[0-9a-f]{{8}}\t{identifier}\t100$", candidate_last_line))


def get_candidates_path(folder_name: str) -> Iterator[tuple[str, str]]:
    for file_name in listdir(folder_name):
        if bool(re.search(".[0-9a-f]{2}.txt$", file_name)):
            identifier = re.search("[0-9a-f]{2}.txt", file_name).group()[:-4]
            yield path.join(folder_name, file_name), identifier


def resolve_collision(file1: str, file2: str) -> str:
    if path.getmtime(file1) < path.getmtime(file2):
        return file1
    return file2


def select_best_solution(folder_name: str, file_name: str) -> str:
    best_candidate = None
    best_zeros_number = 0
    for (candidate_file_name, identifier) in get_candidates_path(folder_name):
        if check_file_structure(identifier, candidate_file_name, file_name):
            ok, zeros_number = check_prefix_sha256(candidate_file_name)
            if ok:
                if zeros_number > best_zeros_number:
                    best_zeros_number = zeros_number
                    best_candidate = candidate_file_name
                elif zeros_number == best_zeros_number:
                   best_candidate = resolve_collision(candidate_file_name, best_candidate)
    return best_candidate


if __name__ == "__main__":
    print(select_best_solution(sys.argv[1], sys.argv[2]))
