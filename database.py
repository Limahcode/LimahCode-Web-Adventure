import sqlite3
import os
import json
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), 'adventure.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'student',
            track TEXT DEFAULT 'junior',
            stars INTEGER DEFAULT 0,
            badges TEXT DEFAULT '[]',
            completed_lessons TEXT DEFAULT '[]',
            completed_challenges TEXT DEFAULT '[]',
            saved_codes TEXT DEFAULT '{}',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Run migration if track column does not exist
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN track TEXT DEFAULT 'junior'")
    except Exception:
        pass # Column already exists
    
    # Ensure default teacher account exists
    cursor.execute('SELECT id FROM users WHERE email = ?', ('teacher@limahcode.com',))
    teacher = cursor.fetchone()
    if not teacher:
        default_pwd_hash = generate_password_hash('limah2026')
        cursor.execute('''
            INSERT INTO users (fullname, email, password_hash, role, track, stars, badges, completed_lessons, completed_challenges)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            'Teacher Admin',
            'teacher@limahcode.com',
            default_pwd_hash,
            'teacher',
            'all',
            100,
            json.dumps(['html_explorer', 'website_builder', 'junior_web_designer']),
            json.dumps([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]),
            json.dumps([1, 2, 3])
        ))
    
    conn.commit()
    conn.close()

def create_user(fullname, email, password, role='student', track='junior'):
    email = email.strip().lower()
    pwd_hash = generate_password_hash(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (fullname, email, password_hash, role, track)
            VALUES (?, ?, ?, ?, ?)
        ''', (fullname.strip(), email, pwd_hash, role, track))
        conn.commit()
        user_id = cursor.lastrowid
        return user_id, None
    except sqlite3.IntegrityError:
        return None, "Email address already registered. Please log in."
    except Exception as e:
        return None, str(e)
    finally:
        conn.close()

def authenticate_user(email, password):
    email = email.strip().lower()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user['password_hash'], password):
        return dict(user)
    return None

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return dict(user)
    return None

def update_user_progress(user_id, stars=None, badges=None, completed_lessons=None, completed_challenges=None, saved_codes=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    updates = []
    values = []
    
    if stars is not None:
        updates.append('stars = ?')
        values.append(stars)
    if badges is not None:
        updates.append('badges = ?')
        values.append(json.dumps(badges) if isinstance(badges, list) else badges)
    if completed_lessons is not None:
        updates.append('completed_lessons = ?')
        values.append(json.dumps(completed_lessons) if isinstance(completed_lessons, list) else completed_lessons)
    if completed_challenges is not None:
        updates.append('completed_challenges = ?')
        values.append(json.dumps(completed_challenges) if isinstance(completed_challenges, list) else completed_challenges)
    if saved_codes is not None:
        updates.append('saved_codes = ?')
        values.append(json.dumps(saved_codes) if isinstance(saved_codes, dict) else saved_codes)
        
    if updates:
        values.append(user_id)
        sql = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(sql, tuple(values))
        conn.commit()
        
    conn.close()

def get_all_students():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, fullname, email, role, track, stars, badges, completed_lessons, completed_challenges, saved_codes, created_at 
        FROM users 
        WHERE role = 'student'
        ORDER BY stars DESC, id ASC
    ''')
    rows = cursor.fetchall()
    conn.close()
    
    students = []
    for r in rows:
        d = dict(r)
        d['badges'] = json.loads(d['badges']) if d['badges'] else []
        d['completed_lessons'] = json.loads(d['completed_lessons']) if d['completed_lessons'] else []
        d['completed_challenges'] = json.loads(d['completed_challenges']) if d['completed_challenges'] else []
        d['saved_codes'] = json.loads(d['saved_codes']) if d['saved_codes'] else {}
        d['completion_pct'] = round((len(d['completed_lessons']) + len(d['completed_challenges'])) / 13 * 100)
        students.append(d)
    return students
