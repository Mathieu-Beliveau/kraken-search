import concurrent.futures
import re
from argparse import ArgumentParser
from re import Pattern

from tabulate import tabulate
import sys
from pathlib import Path

from searcher import Searcher

CORPUS_LOCATION = '/home/strav/Dev/corpus/'
LOCAL_BIN = '/home/strav/.local/bin/'
PROCESSED_FILENAME = "processed"
EXCEPTION_FILENAME = "exception"

results: list[Searcher] = []


def process_dirs_for_ocr(corpus_path: Path, pattern: Pattern):
    folders = get_folders_to_process(corpus_path)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(lambda folder: search(folder, pattern), folders)
    display_results()


def search(folder: Path, pattern: Pattern):
    searcher = Searcher(folder, pattern)
    searcher.search_regex()
    results.append(searcher)


def display_results():
    filtered_lst = list(filter(lambda result: result.matches_count > 0, results))
    sorted_results = sorted(filtered_lst, key=lambda result: result.matches_count, reverse=True)
    sorted_results_for_print = list(map(lambda result: [result.get_file_name(), result.matches_count,
                                                        result.print_matches()], sorted_results))
    print(tabulate(sorted_results_for_print, headers=['File name', 'Occurrences', 'Lines'], tablefmt='orgtbl'))


def get_folders_to_process(corpus_path: Path) -> list[Path]:
    return list(filter(lambda sub_path: sub_path.is_dir() and is_processed(sub_path), corpus_path.iterdir()))


def is_processed(input_path: Path) -> bool:
    processed_list = list(input_path.rglob("processed*"))
    return len(processed_list) == 1


if __name__ == '__main__':
    argparse = ArgumentParser()
    argparse.add_argument("-s", "--search")
    argparse.add_argument("-c", "--corpus")
    args = argparse.parse_args()
    sys.path.insert(0, '~/.local/bin')
    base_path = Path(args.corpus)
    process_dirs_for_ocr(base_path, re.compile(args.search))

