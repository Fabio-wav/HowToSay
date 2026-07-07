from dataclasses import dataclass

@dataclass
class Video:
    id: int
    hash: str
    name:str
    path: str

@dataclass
class Occurrence:
    sentence: str
    start: float
    end: float
    video: Video

