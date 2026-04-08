"""
database.py — SQLite базасы: пайдаланушылар прогресі, ұпайлар, статистика
"""
import sqlite3
import os
from datetime import datetime, date, timedelta

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kazakh_lit.db')


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id         INTEGER PRIMARY KEY,
        username        TEXT,
        full_name       TEXT,
        grade           INTEGER DEFAULT 0,
        points          INTEGER DEFAULT 0,
        level           INTEGER DEFAULT 1,
        streak          INTEGER DEFAULT 0,
        last_active     TEXT,
        joined_at       TEXT DEFAULT (datetime('now')),
        total_games     INTEGER DEFAULT 0,
        correct_answers INTEGER DEFAULT 0
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS game_history (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id     INTEGER,
        game_type   TEXT,
        score       INTEGER,
        total_q     INTEGER,
        grade       INTEGER DEFAULT 0,
        played_at   TEXT DEFAULT (datetime('now')),
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS completed_topics (
        user_id      INTEGER,
        topic_key    TEXT,
        completed_at TEXT DEFAULT (datetime('now')),
        PRIMARY KEY(user_id, topic_key),
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS viewed_authors (
        user_id     INTEGER,
        author_key  TEXT,
        viewed_at   TEXT DEFAULT (datetime('now')),
        PRIMARY KEY(user_id, author_key),
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS achievements (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id   INTEGER,
        badge     TEXT,
        earned_at TEXT DEFAULT (datetime('now')),
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS daily_facts (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        fact     TEXT,
        shown_at TEXT
    )''')

    conn.commit()
    conn.close()


def get_or_create_user(user_id: int, username: str = None, full_name: str = None) -> dict:
    conn = get_connection()
    c = conn.cursor()
    today = date.today().isoformat()

    row = c.execute('SELECT * FROM users WHERE user_id=?', (user_id,)).fetchone()
    if not row:
        c.execute('INSERT INTO users (user_id, username, full_name, last_active) VALUES (?,?,?,?)',
                  (user_id, username, full_name, today))
        conn.commit()
        row = c.execute('SELECT * FROM users WHERE user_id=?', (user_id,)).fetchone()
    else:
        last = row['last_active']
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        new_streak = (row['streak'] + 1) if last == yesterday else (1 if last != today else row['streak'])
        c.execute('UPDATE users SET last_active=?, streak=?, username=?, full_name=? WHERE user_id=?',
                  (today, new_streak, username or row['username'], full_name or row['full_name'], user_id))
        conn.commit()
        row = c.execute('SELECT * FROM users WHERE user_id=?', (user_id,)).fetchone()

    result = dict(row)
    conn.close()
    return result


def add_points(user_id: int, points: int) -> dict:
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET points=points+? WHERE user_id=?', (points, user_id))
    conn.commit()
    row = c.execute('SELECT * FROM users WHERE user_id=?', (user_id,)).fetchone()

    thresholds = [0, 100, 300, 600, 1000, 1500, 2200, 3000, 4000, 5500, 7500]
    new_level = sum(1 for t in thresholds if row['points'] >= t)
    new_level = max(1, min(new_level, 11))

    if new_level != row['level']:
        c.execute('UPDATE users SET level=? WHERE user_id=?', (new_level, user_id))
        conn.commit()
        row = c.execute('SELECT * FROM users WHERE user_id=?', (user_id,)).fetchone()

    result = dict(row)
    conn.close()
    return result


def save_game_result(user_id: int, game_type: str, score: int, total: int, grade: int = 0):
    conn = get_connection()
    conn.execute('INSERT INTO game_history (user_id, game_type, score, total_q, grade) VALUES (?,?,?,?,?)',
                 (user_id, game_type, score, total, grade))
    conn.execute('UPDATE users SET total_games=total_games+1, correct_answers=correct_answers+? WHERE user_id=?',
                 (score, user_id))
    conn.commit()
    conn.close()


def set_user_grade(user_id: int, grade: int):
    conn = get_connection()
    conn.execute('UPDATE users SET grade=? WHERE user_id=?', (grade, user_id))
    conn.commit()
    conn.close()


def mark_topic_completed(user_id: int, topic_key: str):
    conn = get_connection()
    conn.execute('INSERT OR IGNORE INTO completed_topics (user_id, topic_key) VALUES (?,?)', (user_id, topic_key))
    conn.commit()
    conn.close()


def mark_author_viewed(user_id: int, author_key: str):
    conn = get_connection()
    conn.execute('INSERT OR IGNORE INTO viewed_authors (user_id, author_key) VALUES (?,?)', (user_id, author_key))
    conn.commit()
    conn.close()


def get_user_stats(user_id: int) -> dict:
    conn = get_connection()
    row = conn.execute('SELECT * FROM users WHERE user_id=?', (user_id,)).fetchone()
    if not row:
        conn.close()
        return {}
    user = dict(row)
    topics = conn.execute('SELECT COUNT(*) as cnt FROM completed_topics WHERE user_id=?', (user_id,)).fetchone()['cnt']
    authors = conn.execute('SELECT COUNT(*) as cnt FROM viewed_authors WHERE user_id=?', (user_id,)).fetchone()['cnt']
    games = conn.execute(
        'SELECT game_type, COUNT(*) as cnt, SUM(score) as ts FROM game_history WHERE user_id=? GROUP BY game_type',
        (user_id,)).fetchall()
    badges = conn.execute('SELECT badge FROM achievements WHERE user_id=?', (user_id,)).fetchall()
    conn.close()
    return {**user, 'topics_completed': topics, 'authors_viewed': authors,
            'game_stats': [dict(g) for g in games], 'achievements': [b['badge'] for b in badges]}


def get_top_users(limit: int = 10) -> list:
    conn = get_connection()
    rows = conn.execute(
        'SELECT user_id, full_name, username, points, level, total_games FROM users ORDER BY points DESC LIMIT ?',
        (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def give_achievement(user_id: int, badge: str) -> bool:
    conn = get_connection()
    existing = conn.execute('SELECT id FROM achievements WHERE user_id=? AND badge=?', (user_id, badge)).fetchone()
    if not existing:
        conn.execute('INSERT INTO achievements (user_id, badge) VALUES (?,?)', (user_id, badge))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False


LEVEL_NAMES = {
    1:  ("⭐", "Оқушы"),           2: ("⭐⭐", "Ынталы оқушы"),
    3:  ("🌟", "Білімді"),         4: ("🌟🌟", "Зерделі"),
    5:  ("💫", "Дана"),            6: ("💫💫", "Жетік оқырман"),
    7:  ("🔥", "Әдебиет сүйер"),   8: ("🔥🔥", "Ұлы оқырман"),
    9:  ("👑", "Әдебиет шебері"),  10: ("👑💎", "Ұлт данасы"),
    11: ("🏆", "Қазақ Әдебиеті Ұстасы"),
}


def get_level_info(level: int) -> tuple:
    """Деңгей emoji мен атауын қайтарады: (emoji, name)"""
    return LEVEL_NAMES.get(level, ("⭐", "Оқушы"))
