from dataclasses import dataclass, field


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
    words: list[Word] = field(default_factory=list)


@dataclass
class SearchResult:
    sentence: str
    start: float
    end: float
    video: Video
    words: list[Word] = field(default_factory=list)
    transcript: list[Occurrence] = field(default_factory=list)