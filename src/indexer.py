import json
from pathlib import Path

from src.models import Occurrence, Word
from src.sentence_builder import SentenceBuilder


class TranscriptIndexer:

    def __init__(self):
        self.sentence_builder = SentenceBuilder()

    def index_file(self, transcript_path: Path) -> list[Occurrence]:

        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript = json.load(f)

        occurrences = []

        for segment in transcript["segments"]:

            words = [
                Word(
                    text=word["word"].strip(),
                    start=word["start"],
                    end=word["end"]
                )
                for word in segment["words"]
            ]

            sentences = self.sentence_builder.build(words)

            for sentence in sentences:
                print(f"[{sentence.start:.2f} - {sentence.end:.2f}] {sentence.text}")

                occurrences.append(
                    Occurrence(
                        sentence=sentence.text,
                        start=sentence.start,
                        end=sentence.end
                    )
                )

        return occurrences