import sqlite3
import hashlib

from src.models import Occurrence, SearchResult, Video

class Database:

    def __init__(self, db_name="database.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")

    def create_tables(self):

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS videos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hash TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                path TEXT NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS occurrences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id INTEGER NOT NULL,
                sentence TEXT NOT NULL,
                start REAL NOT NULL,
                end REAL NOT NULL,
                FOREIGN KEY(video_id) REFERENCES videos(id)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                occurrence_id INTEGER NOT NULL,
                word TEXT NOT NULL,
                FOREIGN KEY(occurrence_id) REFERENCES occurrences(id)
            )
        """)

        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_occurrences_video_id
            ON occurrences(video_id)
        """)

        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_words_word
            ON words(word)
        """)

        self.connection.commit()

    def insert_occurrence(self, occurrence: Occurrence, video_id: int) -> int:

        self.cursor.execute("""
            INSERT INTO occurrences
            (video_id, sentence, start, end)
            VALUES (?, ?, ?, ?)
        """, (
            video_id,
            occurrence.sentence,
            occurrence.start,
            occurrence.end
        ))

        return self.cursor.lastrowid

    def search(self, query: str) -> list[SearchResult]:

        words = [
            word.strip(".,!?;:\"'()[]{}").lower()
            for word in query.split()
            if word.strip()
        ]

        if not words:
            return []

        placeholders = ",".join("?" * len(words))

        self.cursor.execute(f"""
            SELECT
                o.id,
                o.sentence,
                o.start,
                o.end,
                v.id,
                v.hash,
                v.name,
                v.path
            FROM words w
            INNER JOIN occurrences o
                ON w.occurrence_id = o.id
            INNER JOIN videos v
                ON o.video_id = v.id
            WHERE w.word IN ({placeholders})
            GROUP BY o.id
            HAVING COUNT(DISTINCT w.word) = ?
        """, (*words, len(words)))

        rows = self.cursor.fetchall()

        results = []

        for row in rows:

            video = Video(
                id=row[4],
                hash=row[5],
                name=row[6],
                path=row[7]
            )

            results.append(
                SearchResult(
                    sentence=row[1],
                    start=row[2],
                    end=row[3],
                    video=video
                )
            )

        return results

    def close(self):
        self.connection.close()

    def commit(self):
        self.connection.commit()

    def insert_video(self, file_hash, name, path):

        self.cursor.execute("""
            INSERT OR IGNORE INTO videos(hash, name, path)
            VALUES (?, ?, ?)
        """, (file_hash, name, str(path)))


    def calculate_hash(self, file_path):

        sha = hashlib.sha256()

        with open(file_path, "rb") as f:

            while chunk := f.read(8192):
                sha.update(chunk)

        return sha.hexdigest()
    
    def get_video_id(self, file_hash):

        self.cursor.execute("""
            SELECT id
            FROM videos
            WHERE hash = ?
        """, (file_hash,))

        return self.cursor.fetchone()[0]
    
    def video_exists(self, file_hash: str) -> bool:
        self.cursor.execute("""
            SELECT 1
            FROM videos
            WHERE hash = ?
        """, (file_hash,))

        return self.cursor.fetchone() is not None
    
    def insert_word(self, occurrence_id: int, word: str):

        self.cursor.execute("""
            INSERT INTO words (occurrence_id, word)
            VALUES (?, ?)
        """, (
            occurrence_id,
            word.lower()
        ))