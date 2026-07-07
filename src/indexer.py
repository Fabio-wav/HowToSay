import json
import re
from pathlib import Path

from src.models import Occurrence


class TranscriptIndexer:

    def __init__(self):
        self.word_regex = re.compile(r"[A-Za-z']+")
        self.occurrences = []

    def index_file(self, transcript_path: Path, video_name: str):

        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript = json.load(f)

        occurrences = []

        for segment in transcript["segments"]:

            sentence = segment["text"].strip()

            occurrences.append(
                Occurrence(
                    sentence=sentence,
                    video=video_name,
                    start=segment["start"],
                    end=segment["end"]
                )
            )
        self.occurrences.extend(occurrences)
        return occurrences

    def search(self, query: str):
        query = query.lower()

        return [
            occurrence
            for occurrence in self.occurrences
            if occurrence.word == query
        ]