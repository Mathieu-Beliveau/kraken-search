import re
from pathlib import Path
from re import Pattern

from search_match import SearchMatch


class Searcher:

    def __init__(self, text_path: Path, pattern: Pattern):
        self.matches = []
        self.matches_count = 0
        self.txt_file = self.__get_txt(text_path)
        self.pattern = pattern

    def get_file_name(self):
        return self.txt_file.name

    def print_matches(self) -> str:
        res = ""
        sorted_matches = sorted(self.matches, key=lambda elm: elm.occurrences, reverse=True)
        for match in sorted_matches:
            res += f"Line: {match.line_number}, count: {match.occurrences}\n"
        return res

    def search_regex(self):

        line_number = 0
        with open(self.txt_file, "r") as text_file:
            for line in text_file:
                line_number += 1
                matches = re.findall(self.pattern, line)
                matches_count = len(matches)
                if matches_count > 0:
                    search_match = SearchMatch()
                    search_match.line_number = line_number
                    search_match.line = line
                    search_match.occurrences = matches_count
                    self.matches.append(search_match)
                    self.matches_count += matches_count

    def __get_txt(self, text_path: Path) -> Path:
        txt_list = list(text_path.rglob("*.txt"))
        if len(txt_list) == 1:
            return txt_list[0]
        else:
            raise FileNotFoundError("Could not find ocr result")