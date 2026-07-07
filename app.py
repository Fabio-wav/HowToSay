from config import *
from src.extract_audio import extract_audio
from src.transcribe import transcribe
from src.indexer import TranscriptIndexer
from src.database import Database


def process_file(file, indexer: TranscriptIndexer, db: Database):
    ext = file.suffix.lower()

    if ext not in VIDEO_EXTENSIONS and ext not in AUDIO_EXTENSIONS:
        print(f"Ignorando {file.name}")
        return

    file_hash = db.calculate_hash(file)

    if db.video_exists(file_hash):
        print(f"{file.name} já foi indexado. Pulando...")
        return

    if ext in VIDEO_EXTENSIONS:
        print(f"Processando vídeo: {file.name}")

        audio = AUDIO_DIR / f"{file.stem}.wav"
        extract_audio(file, audio)

        transcript = TRANSCRIPT_DIR / f"{file.stem}.json"
        transcribe(audio, transcript)

    else:
        print(f"Processando áudio: {file.name}")

        transcript = TRANSCRIPT_DIR / f"{file.stem}.json"
        transcribe(file, transcript)

    occurrences = indexer.index_file(
        transcript_path=transcript,
        video_name=file.name
    )

    db.insert_video(
        file_hash=file_hash,
        name=file.name,
        path=file
    )

    video_id = db.get_video_id(file_hash)

    for occurrence in occurrences:
        db.insert_occurrence(occurrence, video_id)

    db.commit()


def main():
    indexer = TranscriptIndexer()

    db = Database()
    db.create_tables()

    files = list(INPUT_DIR.iterdir())

    if not files:
        print("Nenhum arquivo encontrado em videos/input.")
        return

    for file in files:
        process_file(file, indexer, db)

    print("\nTodos os arquivos foram processados!")

    print("\n=== Pesquisa ===")

    query = input("\nDigite uma palavra para pesquisar: ")

    results = db.search(query)

    print(f"\nEncontrados {len(results)} resultados:\n")

    for result in results:
        print(result)

    db.close()


if __name__ == "__main__":
    main()