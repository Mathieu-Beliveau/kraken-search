import logging
import re
from pathlib import Path
from re import Pattern

from search_match import SearchMatch


class Searcher:
    page_match = re.compile(r".*\.pdf\_(.*)")

    def __init__(self, text_path: Path, pattern: Pattern):
        self.text_path = text_path
        self.matches = []
        self.matches_count = 0
        self.pdf_file = self.__get_pdf(text_path)
        self.pattern = pattern

    def get_file_name(self):
        return self.pdf_file.name

    def print_matches(self) -> str:
        res = ""
        sorted_matches = sorted(self.matches, key=lambda elm: elm.page, reverse=False)
        for match in sorted_matches:
            res += f"Page: {match.page}, Line: {match.line_number}, count: {match.occurrences}\n"
        return res

    def search_regex(self):
        files = self.text_path.rglob("*.pdf_*")
        matcher = r"^[^.].*\.pdf_*"
        files = list(filter(lambda pdf: re.search(matcher, pdf.name) is not None, files))
        for file in files:
            line_number = 0
            with open(file, "r") as text_file:
                for line in text_file:
                    try:
                        line_number += 1
                        matches = re.findall(self.pattern, line)
                        matches_count = len(matches)
                        if matches_count > 0:
                            search_match = SearchMatch()
                            re_page_match = self.page_match.search(file.name)
                            search_match.page = re_page_match.groups()[0]
                            search_match.line_number = line_number
                            search_match.line = line
                            search_match.occurrences = matches_count
                            self.matches.append(search_match)
                            self.matches_count += matches_count
                    except:
                        print(f"Could not parse line {line} of file: {file}")

    def __get_pdf(self, input_path: Path) -> Path:
        pdf_list = list(input_path.rglob("*.pdf"))
        matcher = r"^[^.].*\.pdf"
        pdf_list = list(filter(lambda pdf: re.search(matcher, pdf.name) is not None, pdf_list))
        if len(pdf_list) == 1:
            return pdf_list[0]
        else:
            raise FileNotFoundError("Could not find ocr result")