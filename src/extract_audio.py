import subprocess
from pathlib import Path


from pathlib import Path
import subprocess

from config import FFMPEG


def extract_audio(video_path: Path, output_path: Path):

    output_path.parent.mkdir(parents=True, exist_ok=True)

    subprocess.run([
        str(FFMPEG),   # <-- usa o caminho configurado
        "-y",
        "-i",
        str(video_path),
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        "16000",
        "-ac",
        "1",
        str(output_path)
    ], check=True)

    return output_path