import os
import json
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE_URL = os.environ.get('DATABASE_URL')
USE_POSTGRES = False

if DATABASE_URL:
    try:
        import psycopg2
        import psycopg2.extras
        USE_POSTGRES = True
        # Handle Render postgres url compatibility (postgres:// -> postgresql://)
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    except ImportError:
        USE_POSTGRES = False

DB_PATH = os.path.join(os.path.dirname(__file__), 'adventure.db')

def get_db_connection():
    if USE_POSTGRES:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    else:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

def get_cursor(conn):
    if USE_POSTGRES:
        import psycopg2.extras
        return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return conn.cursor()

def init_db():
    conn = get_db_connection()
    cursor = get_cursor(conn)
    
    if USE_POSTGRES:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
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
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservations (
                id SERIAL PRIMARY KEY,
                fullname TEXT NOT NULL,
                track TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                experience TEXT,
                status TEXT DEFAULT 'new',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS page_views (
                id SERIAL PRIMARY KEY,
                event_type TEXT NOT NULL,
                page TEXT NOT NULL,
                device TEXT,
                referrer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
    else:
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
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname TEXT NOT NULL,
                track TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                experience TEXT,
                status TEXT DEFAULT 'new',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS page_views (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                page TEXT NOT NULL,
                device TEXT,
                referrer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN track TEXT DEFAULT 'junior'")
        except Exception:
            pass

    # Ensure default teacher account exists
    ph = '%s' if USE_POSTGRES else '?'
    cursor.execute(f'SELECT id FROM users WHERE email = {ph}', ('teacher@limahcode.com',))
    teacher = cursor.fetchone()
    if not teacher:
        default_pwd_hash = generate_password_hash('limah2026')
        cursor.execute(f'''
            INSERT INTO users (fullname, email, password_hash, role, track, stars, badges, completed_lessons, completed_challenges)
            VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph})
        ''', (
            'Teacher Admin',
            'teacher@limahcode.com',
            default_pwd_hash,
            'teacher',
            'all',
            0,
            json.dumps([]),
            json.dumps([]),
            json.dumps([])
        ))
    else:
        cursor.execute('''
            UPDATE users SET completed_lessons = '[]', completed_challenges = '[]', badges = '[]', stars = 0
            WHERE email = 'teacher@limahcode.com' AND role = 'teacher'
        ''')
    
    conn.commit()
    conn.close()

def create_user(fullname, email, password, role='student', track='junior'):
    email = email.strip().lower()
    pwd_hash = generate_password_hash(password)
    conn = get_db_connection()
    cursor = get_cursor(conn)
    ph = '%s' if USE_POSTGRES else '?'
    
    try:
        if USE_POSTGRES:
            cursor.execute(f'''
                INSERT INTO users (fullname, email, password_hash, role, track)
                VALUES ({ph}, {ph}, {ph}, {ph}, {ph}) RETURNING id
            ''', (fullname.strip(), email, pwd_hash, role, track))
            user_id = cursor.fetchone()['id']
        else:
            cursor.execute(f'''
                INSERT INTO users (fullname, email, password_hash, role, track)
                VALUES ({ph}, {ph}, {ph}, {ph}, {ph})
            ''', (fullname.strip(), email, pwd_hash, role, track))
            user_id = cursor.lastrowid
            
        conn.commit()
        return user_id, None
    except Exception as e:
        err_msg = str(e).lower()
        if "unique" in err_msg or "duplicate key" in err_msg or "integrityerror" in err_msg:
            return None, "Email address already registered. Please log in."
        return None, str(e)
    finally:
        conn.close()

def authenticate_user(email, password):
    email = email.strip().lower()
    conn = get_db_connection()
    cursor = get_cursor(conn)
    ph = '%s' if USE_POSTGRES else '?'
    
    cursor.execute(f'SELECT * FROM users WHERE email = {ph}', (email,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user['password_hash'], password):
        return dict(user)
    return None

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = get_cursor(conn)
    ph = '%s' if USE_POSTGRES else '?'
    
    cursor.execute(f'SELECT * FROM users WHERE id = {ph}', (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return dict(user)
    return None

def update_user_progress(user_id, stars=None, badges=None, completed_lessons=None, completed_challenges=None, saved_codes=None):
    conn = get_db_connection()
    cursor = get_cursor(conn)
    ph = '%s' if USE_POSTGRES else '?'
    
    updates = []
    values = []
    
    if stars is not None:
        updates.append(f'stars = {ph}')
        values.append(stars)
    if badges is not None:
        updates.append(f'badges = {ph}')
        values.append(json.dumps(badges) if isinstance(badges, list) else badges)
    if completed_lessons is not None:
        updates.append(f'completed_lessons = {ph}')
        values.append(json.dumps(completed_lessons) if isinstance(completed_lessons, list) else completed_lessons)
    if completed_challenges is not None:
        updates.append(f'completed_challenges = {ph}')
        values.append(json.dumps(completed_challenges) if isinstance(completed_challenges, list) else completed_challenges)
    if saved_codes is not None:
        updates.append(f'saved_codes = {ph}')
        values.append(json.dumps(saved_codes) if isinstance(saved_codes, dict) else saved_codes)
        
    if updates:
        values.append(user_id)
        sql = f"UPDATE users SET {', '.join(updates)} WHERE id = {ph}"
        cursor.execute(sql, tuple(values))
        conn.commit()
        
    conn.close()

def get_all_students():
    conn = get_db_connection()
    cursor = get_cursor(conn)
    ph = '%s' if USE_POSTGRES else '?'
    
    cursor.execute(f'''
        SELECT id, fullname, email, role, track, stars, badges, completed_lessons, completed_challenges, saved_codes, created_at 
        FROM users 
        WHERE role = {ph}
        ORDER BY stars DESC, id ASC
    ''', ('student',))
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

def create_reservation(fullname, track, phone, email, experience=''):
    conn = get_db_connection()
    cursor = get_cursor(conn)
    ph = '%s' if USE_POSTGRES else '?'
    try:
        cursor.execute(f'''
            INSERT INTO reservations (fullname, track, phone, email, experience)
            VALUES ({ph}, {ph}, {ph}, {ph}, {ph})
        ''', (fullname.strip(), track.strip(), phone.strip(), email.strip().lower(), (experience or '').strip()))
        conn.commit()
        return True, None
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def get_all_reservations():
    conn = get_db_connection()
    cursor = get_cursor(conn)
    cursor.execute('SELECT * FROM reservations ORDER BY created_at DESC')
    rows = cursor.fetchall()
    conn.close()
    
    reservations = []
    for r in rows:
        d = dict(r)
        if 'created_at' in d and d['created_at']:
            d['created_at_str'] = str(d['created_at'])[:16]
        else:
            d['created_at_str'] = ''
        reservations.append(d)
    return reservations

def delete_reservation(res_id):
    conn = get_db_connection()
    cursor = get_cursor(conn)
    ph = '%s' if USE_POSTGRES else '?'
    try:
        cursor.execute(f'DELETE FROM reservations WHERE id = {ph}', (res_id,))
        conn.commit()
        return True, None
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def record_analytics_event(event_type, page, device='', referrer=''):
    conn = get_db_connection()
    cursor = get_cursor(conn)
    ph = '%s' if USE_POSTGRES else '?'
    try:
        cursor.execute(f'''
            INSERT INTO page_views (event_type, page, device, referrer)
            VALUES ({ph}, {ph}, {ph}, {ph})
        ''', (event_type.strip(), page.strip() or 'index.html', device.strip() or 'Desktop', referrer.strip()))
        conn.commit()
        return True, None
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def get_analytics_summary():
    conn = get_db_connection()
    cursor = get_cursor(conn)
    
    # Total page views
    cursor.execute("SELECT COUNT(*) as count FROM page_views WHERE event_type = 'pageview'")
    row = cursor.fetchone()
    total_views = row['count'] if row else 0

    # Total WhatsApp clicks
    cursor.execute("SELECT COUNT(*) as count FROM page_views WHERE event_type = 'whatsapp_click'")
    row = cursor.fetchone()
    total_wa_clicks = row['count'] if row else 0

    # Mobile vs Desktop
    cursor.execute("SELECT device, COUNT(*) as count FROM page_views GROUP BY device")
    device_rows = cursor.fetchall() or []
    devices = {r['device']: r['count'] for r in device_rows}

    # Top visited pages
    cursor.execute("SELECT page, COUNT(*) as count FROM page_views WHERE event_type = 'pageview' GROUP BY page ORDER BY count DESC LIMIT 8")
    page_rows = cursor.fetchall() or []
    top_pages = [{'page': r['page'], 'views': r['count']} for r in page_rows]

    conn.close()
    return {
        'total_views': total_views,
        'total_wa_clicks': total_wa_clicks,
        'devices': devices,
        'top_pages': top_pages
    }



