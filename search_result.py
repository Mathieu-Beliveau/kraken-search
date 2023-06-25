from search_match import SearchMatch


class SearchResult:
    matches: list[SearchMatch] = []
    matches_count: int = 0
    file_name: str

    def __init__(self, file_name):
        self.file_name = file_name

    def add_match(self, match: SearchMatch, count):
        self.matches.append(match)
        self.matches_count += count