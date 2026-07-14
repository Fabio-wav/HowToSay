from faster_whisper import WhisperModel
import json
from pathlib import Path

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)


def transcribe(audio_path: Path, output_json: Path):

    segments, info = model.transcribe(
        str(audio_path),
        language="en",
        word_timestamps=True
    )

    result = {
        "language": info.language,
        "segments": []
    }

    for segment in segments:
        result["segments"].append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text,
            "words": [
                {
                    "word": word.word,
                    "start": word.start,
                    "end": word.end
                }
                for word in segment.words
            ]
        })

    output_json.parent.mkdir(parents=True, exist_ok=True)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    return result