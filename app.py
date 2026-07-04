from config import *
from src.extract_audio import extract_audio
from src.transcribe import transcribe
from src.indexer import TranscriptIndexer

indexer = TranscriptIndexer()

files = list(INPUT_DIR.iterdir())

if not files:
    print("Nenhum arquivo encontrado em videos/input.")
    exit()

for file in files:

    ext = file.suffix.lower()

    if ext in VIDEO_EXTENSIONS:

        print(f"Processando vídeo: {file.name}")

        audio = AUDIO_DIR / f"{file.stem}.wav"

        extract_audio(file, audio)

        transcript = TRANSCRIPT_DIR / f"{file.stem}.json"

        transcribe(audio, transcript)

    elif ext in AUDIO_EXTENSIONS:

        print(f"Processando áudio: {file.name}")

        transcript = TRANSCRIPT_DIR / f"{file.stem}.json"

        transcribe(file, transcript)

    else:
        print(f"Ignorando {file.name}")
        continue

    # Indexa as ocorrências do arquivo
    indexer.index_file(
        transcript_path=transcript,
        video_name=file.name
    )

print("\nTodos os arquivos foram processados!")

print("\n=== Pesquisa ===")

query = input("\nDigite uma palavra para pesquisar: ")

results = indexer.search(query)

print(f"\nEncontrados {len(results)} resultados:\n")

for result in results:
    print(result)