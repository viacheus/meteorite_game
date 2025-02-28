import sqlite3
from datetime import datetime


def init_db():
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS settings')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT,
            score INTEGER,
            victory BOOLEAN
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            level_id INTEGER PRIMARY KEY,
            sum_enabled BOOLEAN DEFAULT 1,
            sub_enabled BOOLEAN DEFAULT 1,
            mul_enabled BOOLEAN DEFAULT 0,
            div_enabled BOOLEAN DEFAULT 0,
            complexity INTEGER DEFAULT 5
        )
    ''')

    for level_id in range(1, 6):
        cursor.execute('''
            INSERT OR IGNORE INTO settings 
            (level_id, sum_enabled, sub_enabled, mul_enabled, div_enabled, complexity)
            VALUES (?, 1, 1, 0, 0, ?)
        ''', (level_id, level_id * 2))

    conn.commit()
    return conn


def save_score(conn, player_name, score, victory):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO scores (player_name, score, victory)
        VALUES (?, ?, ?)
    ''', (player_name, score, victory))
    conn.commit()


def get_high_scores(conn, limit=10):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM scores ORDER BY score DESC LIMIT ?', (limit,))
    return cursor.fetchall()


def save_settings(conn, level_id, settings):
    cursor = conn.cursor()
    cursor.execute('SELECT level_id FROM settings WHERE level_id = ?', (level_id,))
    exists = cursor.fetchone()

    if exists:
        cursor.execute('''
            UPDATE settings 
            SET sum_enabled = ?, sub_enabled = ?, mul_enabled = ?, 
                div_enabled = ?, complexity = ?
            WHERE level_id = ?
        ''', (settings['sum'], settings['sub'], settings['mul'],
              settings['div'], settings['complexity'], level_id))
    else:
        cursor.execute('''
            INSERT INTO settings 
            (level_id, sum_enabled, sub_enabled, mul_enabled, div_enabled, complexity)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (level_id, settings['sum'], settings['sub'],
              settings['mul'], settings['div'], settings['complexity']))
    conn.commit()


def get_settings(conn, level_id):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM settings WHERE level_id = ?', (level_id,))
    return cursor.fetchone()
