from pathlib import Path

BASE_DIR = Path(__file__).parent

FFMPEG = BASE_DIR / "ffmpeg" / "ffmpeg.exe"

VIDEOS_DIR = BASE_DIR / "videos"
INPUT_DIR = VIDEOS_DIR / "input"
AUDIO_DIR = VIDEOS_DIR / "audio"

OUTPUT_DIR = BASE_DIR / "output"
TRANSCRIPT_DIR = OUTPUT_DIR / "transcripts"

VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".mkv",
    ".avi",
    ".webm"
}

AUDIO_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".m4a",
    ".aac",
    ".flac",
    ".ogg"
}