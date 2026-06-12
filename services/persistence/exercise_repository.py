import sqlite3
import streamlit as st
from pathlib import Path


_DB_PATH = str(Path(__file__).parent.parent.parent / "data.db")

# streamlit runs multiple script executions; cache a single connection per app runtime
@st.cache_resource
def _get_connection():
  conn = sqlite3.connect(_DB_PATH, check_same_thread=False)
  conn.row_factory = sqlite3.Row

  # Ensure required tables exist and migrate any outdated exercises schema.
  with conn:
    conn.execute("""
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    """)

    conn.execute("""
      CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES users(id),
        exercise_name TEXT NOT NULL,
        reps INTEGER NOT NULL DEFAULT 0,
        sets INTEGER NOT NULL DEFAULT 0,
        time INTEGER NOT NULL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    """)

    _migrate_exercises_schema(conn)

  return conn


def _migrate_exercises_schema(conn):
  info = conn.execute("PRAGMA table_info(exercises)").fetchall()
  if not info:
    return

  column_names = [row[1] for row in info]
  if "user_id" in column_names:
    return

  # Old exercises table exists with a legacy schema. Replace it with the current schema.
  conn.execute("ALTER TABLE exercises RENAME TO exercises_old")
  conn.execute("""
      CREATE TABLE exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES users(id),
        exercise_name TEXT NOT NULL,
        reps INTEGER NOT NULL DEFAULT 0,
        sets INTEGER NOT NULL DEFAULT 0,
        time INTEGER NOT NULL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    """)
  conn.execute("DROP TABLE IF EXISTS exercises_old")


def init_db():
  """Compatibility wrapper: ensure the connection is created and tables exist."""
  _get_connection()

def get_user(username):
  conn = _get_connection()
  return conn.execute("""SELECT * FROM users WHERE username = ?""", (username,)).fetchone()

def create_user(username):
  conn = _get_connection()
  with conn:
    conn.execute("""INSERT INTO users (username) VALUES (?)""", (username,))

    return get_user(username)
  
def get_or_create_user(username):
  
  user = get_user(username)
  
  if user is None:
    return create_user(username)
  return user

def add_exercise(user_id, exercise_name, reps, sets, time):
  conn = _get_connection()
  
  with conn:
    exiting = conn.execute("""
      SELECT * FROM exercises WHERE user_id = ? AND exercise_name = ? AND DATE(created_at) = DATE('now')
    """, (user_id, exercise_name)).fetchone() #we want to update the existing record if the user is doing the same exercise within the same day, otherwise we will create a new record for each set of exercises, which is not what we want. We want to track the total reps, sets and time for each exercise per day.
    
    if exiting:
      conn.execute("""
        UPDATE exercises SET reps = reps + ?, sets = sets + ?, time = time + ? WHERE id = ?
      """, (reps, sets, time, exiting["id"]))
    else:
      conn.execute("""
        INSERT INTO exercises (user_id, exercise_name, reps, sets, time) VALUES (?, ?, ?, ?, ?)
      """, (user_id, exercise_name, reps, sets, time))
      
def get_users_exercises(user_id):
  conn = _get_connection()
  
  return conn.execute("""
    SELECT * FROM exercises 
    WHERE user_id = ?
  """, (user_id,)).fetchall()