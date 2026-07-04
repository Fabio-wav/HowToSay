from dataclasses import dataclass


@dataclass
class Occurrence:
    word: str
    sentence: str
    video: str
    start: float
    end: float