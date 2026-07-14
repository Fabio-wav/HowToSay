from dataclasses import dataclass


@dataclass
class Video:
    id: int
    hash: str
    name: str
    path: str


@dataclass
class Word:
    text: str
    start: float
    end: float


@dataclass
class Sentence:
    text: str
    start: float
    end: float
    words: list[Word]


@dataclass
class Occurrence:
    sentence: str
    start: float
    end: float

@dataclass
class SearchResult:
    sentence: str
    start: float
    end: float
    video: Video