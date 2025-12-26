import sqlite3
import json
import os
from datetime import datetime

DB_NAME = os.path.join(os.path.dirname(__file__), "study_hub.db")

class Database:
    @staticmethod
    def connect():
        return sqlite3.connect(DB_NAME)

    @staticmethod
    def initialize():
        con = Database.connect()
        cur = con.cursor()
        
        # Vocabulary Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vocabulary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL,
                meaning TEXT NOT NULL,
                example TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Study Timer Session Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS study_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                duration_seconds INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # MCQs Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS mcqs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                options_json TEXT NOT NULL,
                correct_index INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        con.commit()
        con.close()

    # --- Vocabulary Methods ---
    @staticmethod
    def add_word(word, meaning, example=""):
        con = Database.connect()
        cur = con.cursor()
        cur.execute("INSERT INTO vocabulary (word, meaning, example) VALUES (?, ?, ?)", (word, meaning, example))
        con.commit()
        con.close()

    @staticmethod
    def get_words():
        con = Database.connect()
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM vocabulary ORDER BY id DESC")
        rows = cur.fetchall()
        con.close()
        return [dict(row) for row in rows]

    @staticmethod
    def delete_word(word_id):
        con = Database.connect()
        cur = con.cursor()
        cur.execute("DELETE FROM vocabulary WHERE id = ?", (word_id,))
        con.commit()
        con.close()

    # --- Timer Methods ---
    @staticmethod
    def log_study_session(seconds):
        con = Database.connect()
        cur = con.cursor()
        cur.execute("INSERT INTO study_sessions (duration_seconds) VALUES (?)", (seconds,))
        con.commit()
        con.close()
        
    @staticmethod
    def get_total_study_time():
        con = Database.connect()
        cur = con.cursor()
        cur.execute("SELECT SUM(duration_seconds) FROM study_sessions")
        result = cur.fetchone()[0]
        con.close()
        return result if result else 0

    # --- MCQ Methods ---
    @staticmethod
    def add_mcq(question, options, correct_index):
        """
        options: list of strings
        correct_index: 1-based index (1-4)
        """
        con = Database.connect()
        cur = con.cursor()
        cur.execute("INSERT INTO mcqs (question, options_json, correct_index) VALUES (?, ?, ?)", 
                    (question, json.dumps(options), correct_index))
        con.commit()
        con.close()

    @staticmethod
    def get_mcqs():
        con = Database.connect()
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM mcqs ORDER BY id DESC")
        rows = cur.fetchall()
        con.close()
        results = []
        for row in rows:
            d = dict(row)
            d['options'] = json.loads(d['options_json'])
            results.append(d)
        return results
    
    @staticmethod
    def get_random_mcq():
        con = Database.connect()
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM mcqs ORDER BY RANDOM() LIMIT 1")
        row = cur.fetchone()
        con.close()
        if row:
            d = dict(row)
            d['options'] = json.loads(d['options_json'])
            return d
        return None

    @staticmethod
    def get_stats():
        con = Database.connect()
        cur = con.cursor()
        
        cur.execute("SELECT COUNT(*) FROM vocabulary")
        vocab_count = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM mcqs")
        mcq_count = cur.fetchone()[0]
        
        cur.execute("SELECT SUM(duration_seconds) FROM study_sessions")
        total_seconds = cur.fetchone()[0]
        
        con.close()
        return {
            "vocab_count": vocab_count,
            "mcq_count": mcq_count,
            "total_seconds": total_seconds if total_seconds else 0
        }

# Auto-initialize on import/run
Database.initialize()
