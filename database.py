import sqlite3


def create_database():

    conn = sqlite3.connect("predictions.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        image_name TEXT,

        disease TEXT,

        confidence REAL,

        prediction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()

    conn.close()


def save_prediction(image_name, disease, confidence):

    conn = sqlite3.connect("predictions.db")

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions(image_name, disease, confidence)
        VALUES (?, ?, ?)
    """, (image_name, disease, confidence))

    conn.commit()

    conn.close()


def get_predictions():

    conn = sqlite3.connect("predictions.db")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM predictions
        ORDER BY prediction_time DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


create_database()