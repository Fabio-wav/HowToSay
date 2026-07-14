def __init__(self, db_name="database.db"):
    self.connection = sqlite3.connect(db_name)
    self.cursor = self.connection.cursor()

    self.cursor.execute("PRAGMA foreign_keys = ON")

