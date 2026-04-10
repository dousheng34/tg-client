"""
database.py — SQLite (жергілікті) / PostgreSQL (Koyeb + Supabase) қолдауы
DATABASE_URL env орнатылса → PostgreSQL (Supabase)
Орнатылмаса          → SQLite (жергілікті тестілеу)
"""
import os
import logging
from datetime import datetime, date, timedelta

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv('DATABASE_URL', '').strip()
USE_PG       = bool(DATABASE_URL)
SQLITE_PATH  = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kazakh_lit.db')

logger.info(f"🗄️ Дерекқор режимі: {'PostgreSQL (Supabase)' if USE_PG else 'SQLite (жергілікті)'}")


# ─── PostgreSQL адаптері ──────────────────────────────────────────────────────

def _normalize_sql(sql: str) -> str:
    """SQLite синтаксисін PostgreSQL-ге ауыстырады"""
    sql = sql.replace('?', '%s')
    sql = sql.replace('INTEGER PRIMARY KEY AUTOINCREMENT', 'BIGINT PRIMARY KEY')
    sql = sql.replace('SERIAL PRIMARY KEY', 'BIGINT PRIMARY KEY')
    sql = sql.replace("datetime('now')", "NOW()::TEXT")
    sql = sql.replace('AUTOINCREMENT', '')
    return sql


class _PGCursor:
    """psycopg2 cursor → sqlite3-тей жұмыс жасайды"""
    def __init__(self, raw_cur):
        self._c = raw_cur

    def execute(self, sql, params=()):
        had_oi = 'INSERT OR IGNORE' in sql
        sql = sql.replace('INSERT OR IGNORE INTO', 'INSERT INTO')
        sql = _normalize_sql(sql)
        if had_oi:
            sql = sql.rstrip(';') + ' ON CONFLICT DO NOTHING'
        self._c.execute(sql, params or ())
        return self

    def fetchone(self):
        row = self._c.fetchone()
        return dict(row) if row else None

    def fetchall(self):
        return [dict(r) for r in (self._c.fetchall() or [])]


class _PGConn:
    """psycopg2 connection → sqlite3-тей жұмыс жасайды"""
    def __init__(self, raw_conn):
        import psycopg2.extras
        self._conn   = raw_conn
        self._extras = psycopg2.extras
        self.row_factory = None   # sqlite3 compat

    def cursor(self):
        return _PGCursor(
            self._conn.cursor(cursor_factory=self._extras.RealDictCursor)
        )

    def execute(self, sql, params=()):
        """sqlite3 conn.execute() shorthand"""
        cur = self.cursor()
        cur.execute(sql, params)
        return cur

    def commit(self):
        self._conn.commit()

    def close(self):
        self._conn.close()


# ─── Қосылым ─────────────────────────────────────────────────────────────────

def get_connection():
    if USE_PG:
        import psycopg2
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = False
        return _PGConn(conn)
    else:
        import sqlite3
        conn = sqlite3.connect(SQLITE_PATH)
        conn.row_factory = sqlite3.Row
        return conn


# ─── Кесте жасау ─────────────────────────────────────────────────────────────

def init_db():
    conn = get_connection()
    c    = conn.cursor()

    # users
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id         BIGINT PRIMARY KEY,
        username        TEXT,
        full_name       TEXT,
        grade           INTEGER DEFAULT 0,
        points          INTEGER DEFAULT 0,
        level           INTEGER DEFAULT 1,
        streak          INTEGER DEFAULT 0,
        last_active     TEXT,
        joined_at       TEXT,
        total_games     INTEGER DEFAULT 0,
        correct_answers INTEGER DEFAULT 0
    )''' if USE_PG else '''CREATE TABLE IF NOT EXISTS users (
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

    # game_history
    c.execute('''CREATE TABLE IF NOT EXISTS game_history (
        id          BIGSERIAL PRIMARY KEY,
        user_id     BIGINT,
        game_type   TEXT,
        score       INTEGER,
        total_q     INTEGER,
        grade       INTEGER DEFAULT 0,
        played_at   TEXT
    )''' if USE_PG else '''CREATE TABLE IF NOT EXISTS game_history (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id     INTEGER,
        game_type   TEXT,
        score       INTEGER,
        total_q     INTEGER,
        grade       INTEGER DEFAULT 0,
        played_at   TEXT DEFAULT (datetime('now'))
    )''')

    # completed_topics
    c.execute('''CREATE TABLE IF NOT EXISTS completed_topics (
        user_id      BIGINT,
        topic_key    TEXT,
        completed_at TEXT,
        PRIMARY KEY(user_id, topic_key)
    )''' if USE_PG else '''CREATE TABLE IF NOT EXISTS completed_topics (
        user_id      INTEGER,
        topic_key    TEXT,
        completed_at TEXT DEFAULT (datetime('now')),
        PRIMARY KEY(user_id, topic_key)
    )''')

    # viewed_authors
    c.execute('''CREATE TABLE IF NOT EXISTS viewed_authors (
        user_id     BIGINT,
        author_key  TEXT,
        viewed_at   TEXT,
        PRIMARY KEY(user_id, author_key)
    )''' if USE_PG else '''CREATE TABLE IF NOT EXISTS viewed_authors (
        user_id     INTEGER,
        author_key  TEXT,
        viewed_at   TEXT DEFAULT (datetime('now')),
        PRIMARY KEY(user_id, author_key)
    )''')

    # achievements
    c.execute('''CREATE TABLE IF NOT EXISTS achievements (
        id        BIGSERIAL PRIMARY KEY,
        user_id   BIGINT,
        badge     TEXT,
        earned_at TEXT
    )''' if USE_PG else '''CREATE TABLE IF NOT EXISTS achievements (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id   INTEGER,
        badge     TEXT,
        earned_at TEXT DEFAULT (datetime('now'))
    )''')

    # feedbacks
    c.execute('''CREATE TABLE IF NOT EXISTS feedbacks (
        id         BIGSERIAL PRIMARY KEY,
        user_id    BIGINT,
        username   TEXT,
        full_name  TEXT,
        category   TEXT,
        text       TEXT,
        created_at TEXT
    )''' if USE_PG else '''CREATE TABLE IF NOT EXISTS feedbacks (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id    INTEGER,
        username   TEXT,
        full_name  TEXT,
        category   TEXT,
        text       TEXT,
        created_at TEXT DEFAULT (datetime('now'))
    )''')

    conn.commit()
    conn.close()
    logger.info("✅ Барлық кестелер дайын")


# ─── Пайдаланушы ─────────────────────────────────────────────────────────────

def get_or_create_user(user_id: int, username: str = None, full_name: str = None) -> dict:
    conn = get_connection()
    c    = conn.cursor()
    today     = date.today().isoformat()
    now_txt   = datetime.now().isoformat(timespec='seconds')

    row = c.execute('SELECT * FROM users WHERE user_id=?', (user_id,)).fetchone()
    if not row:
        c.execute(
            'INSERT INTO users (user_id, username, full_name, last_active, joined_at) VALUES (?,?,?,?,?)',
            (user_id, username, full_name, today, now_txt)
        )
        conn.commit()
        row = c.execute('SELECT * FROM users WHERE user_id=?', (user_id,)).fetchone()
    else:
        last      = row['last_active']
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        new_streak = (row['streak'] + 1) if last == yesterday else (1 if last != today else row['streak'])
        c.execute(
            'UPDATE users SET last_active=?, streak=?, username=?, full_name=? WHERE user_id=?',
            (today, new_streak, username or row['username'], full_name or row['full_name'], user_id)
        )
        conn.commit()
        row = c.execute('SELECT * FROM users WHERE user_id=?', (user_id,)).fetchone()

    result = dict(row)
    conn.close()
    return result


def add_points(user_id: int, points: int) -> dict:
    conn = get_connection()
    c    = conn.cursor()
    c.execute('UPDATE users SET points=points+? WHERE user_id=?', (points, user_id))
    conn.commit()
    row = c.execute('SELECT * FROM users WHERE user_id=?', (user_id,)).fetchone()

    thresholds = [0, 100, 300, 600, 1000, 1500, 2200, 3000, 4000, 5500, 7500]
    new_level  = sum(1 for t in thresholds if row['points'] >= t)
    new_level  = max(1, min(new_level, 11))

    if new_level != row['level']:
        c.execute('UPDATE users SET level=? WHERE user_id=?', (new_level, user_id))
        conn.commit()
        row = c.execute('SELECT * FROM users WHERE user_id=?', (user_id,)).fetchone()

    result = dict(row)
    conn.close()
    return result


def set_user_grade(user_id: int, grade: int):
    conn = get_connection()
    conn.execute('UPDATE users SET grade=? WHERE user_id=?', (grade, user_id))
    conn.commit()
    conn.close()


# ─── Ойын тарихы ──────────────────────────────────────────────────────────────

def save_game_result(user_id: int, game_type: str, score: int, total: int, grade: int = 0):
    now_txt = datetime.now().isoformat(timespec='seconds')
    conn = get_connection()
    conn.execute(
        'INSERT INTO game_history (user_id, game_type, score, total_q, grade, played_at) VALUES (?,?,?,?,?,?)',
        (user_id, game_type, score, total, grade, now_txt)
    )
    conn.execute(
        'UPDATE users SET total_games=total_games+1, correct_answers=correct_answers+? WHERE user_id=?',
        (score, user_id)
    )
    conn.commit()
    conn.close()


# ─── Тақырыптар / Авторлар ────────────────────────────────────────────────────

def mark_topic_completed(user_id: int, topic_key: str):
    now_txt = datetime.now().isoformat(timespec='seconds')
    conn = get_connection()
    conn.execute(
        'INSERT OR IGNORE INTO completed_topics (user_id, topic_key, completed_at) VALUES (?,?,?)',
        (user_id, topic_key, now_txt)
    )
    conn.commit()
    conn.close()


def mark_author_viewed(user_id: int, author_key: str):
    now_txt = datetime.now().isoformat(timespec='seconds')
    conn = get_connection()
    conn.execute(
        'INSERT OR IGNORE INTO viewed_authors (user_id, author_key, viewed_at) VALUES (?,?,?)',
        (user_id, author_key, now_txt)
    )
    conn.commit()
    conn.close()


# ─── Статистика ──────────────────────────────────────────────────────────────

def get_user_stats(user_id: int) -> dict:
    conn   = get_connection()
    c      = conn.cursor()
    row    = c.execute('SELECT * FROM users WHERE user_id=?', (user_id,)).fetchone()
    if not row:
        conn.close(); return {}
    user   = dict(row)
    topics = c.execute(
        'SELECT COUNT(*) as cnt FROM completed_topics WHERE user_id=?', (user_id,)
    ).fetchone()['cnt']
    authors = c.execute(
        'SELECT COUNT(*) as cnt FROM viewed_authors WHERE user_id=?', (user_id,)
    ).fetchone()['cnt']
    games  = c.execute(
        'SELECT game_type, COUNT(*) as cnt, SUM(score) as ts FROM game_history WHERE user_id=? GROUP BY game_type',
        (user_id,)
    ).fetchall()
    badges = c.execute(
        'SELECT badge FROM achievements WHERE user_id=?', (user_id,)
    ).fetchall()
    conn.close()
    return {
        **user,
        'topics_completed': topics,
        'authors_viewed':   authors,
        'game_stats':       [dict(g) for g in games],
        'achievements':     [b['badge'] for b in badges],
    }


def get_top_users(limit: int = 10) -> list:
    conn = get_connection()
    rows = conn.execute(
        'SELECT user_id, full_name, username, points, level, total_games '
        'FROM users ORDER BY points DESC LIMIT ?',
        (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── Жетістіктер ─────────────────────────────────────────────────────────────

def give_achievement(user_id: int, badge: str) -> bool:
    conn     = get_connection()
    c        = conn.cursor()
    existing = c.execute(
        'SELECT id FROM achievements WHERE user_id=? AND badge=?', (user_id, badge)
    ).fetchone()
    if not existing:
        now_txt = datetime.now().isoformat(timespec='seconds')
        c.execute(
            'INSERT INTO achievements (user_id, badge, earned_at) VALUES (?,?,?)',
            (user_id, badge, now_txt)
        )
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False


# ─── Пікірлер (Feedbacks) ────────────────────────────────────────────────────

def save_feedback(user_id: int, username: str, full_name: str, category: str, text: str):
    """Пайдаланушы пікірін сақтайды"""
    now_txt = datetime.now().isoformat(timespec='seconds')
    conn = get_connection()
    conn.execute(
        'INSERT INTO feedbacks (user_id, username, full_name, category, text, created_at) '
        'VALUES (?,?,?,?,?,?)',
        (user_id, username, full_name, category, text, now_txt)
    )
    conn.commit()
    conn.close()


def get_all_feedbacks(limit: int = 20) -> list:
    """Соңғы пікірлерді қайтарады"""
    conn = get_connection()
    rows = conn.execute(
        'SELECT * FROM feedbacks ORDER BY created_at DESC LIMIT ?', (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── Деңгей атаулары ─────────────────────────────────────────────────────────

LEVEL_NAMES = {
    1:  ("⭐",    "Оқушы"),
    2:  ("⭐⭐",  "Ынталы оқушы"),
    3:  ("🌟",    "Білімді"),
    4:  ("🌟🌟",  "Зерделі"),
    5:  ("💫",    "Дана"),
    6:  ("💫💫",  "Жетік оқырман"),
    7:  ("🔥",    "Әдебиет сүйер"),
    8:  ("🔥🔥",  "Ұлы оқырман"),
    9:  ("👑",    "Әдебиет шебері"),
    10: ("👑💎",  "Ұлт данасы"),
    11: ("🏆",    "Қазақ Әдебиеті Ұстасы"),
}


def get_level_info(level: int) -> tuple:
    return LEVEL_NAMES.get(level, ("⭐", "Оқушы"))
