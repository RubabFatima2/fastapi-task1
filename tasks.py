import os
import psycopg
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg.connect(DATABASE_URL)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        done BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany(
            "INSERT INTO tasks(title, done) VALUES (%s, %s)",
            [
                ("Learn FastAPI", False),
                ("Learn SQLite", True),
                ("Build Todo API", False),
            ],
        )

    connection.commit()
    cursor.close()
    connection.close()

def get_all_tasks(search=None, done=None):
    connection = get_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM tasks"
    
    params = []

    if search:
        query += " WHERE title LIKE %s"
        params.append(f"%{search}%")

    elif done is not None:
        query += " WHERE done = %s"
        params.append(done)

    query += " ORDER BY title ASC"

    cursor.execute(query, params)
        
    rows = cursor.fetchall()

    connection.close()
    return rows
    # connection.commit()


def get_by_id(task_id:int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks where id = %s",(task_id,))
    rows = cursor.fetchone()
    connection.close()
    return rows
    # connection.commit()


def add_task(title: str, done:bool):
   
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
    INSERT INTO tasks(title, done)
    VALUES (%s, %s)
    RETURNING *
    """, (title, done))
    # cursor.execute(
    # "SELECT * FROM tasks WHERE id = last_insert_rowid()")
    task = cursor.fetchone()
    
    
    connection.commit()
    
    connection.close()
    return task


def update_task(id: int, title: str, done: bool):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE tasks
        SET title = %s, done = %s, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s RETURNING *
    """, (title, done, id))
    updated_task = cursor.fetchone()
    connection.commit()
    connection.close()

    return updated_task

def delete_task(id:int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE from tasks WHERE id=%s",(id,))
    connection.commit()
    deleted = cursor.rowcount

    connection.close()
    return deleted 

def get_stats():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE done = TRUE")
    completed = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE done = FALSE")
    pending = cursor.fetchone()[0]
    
    connection.close()

    return {
        "total": total,
        "completed": completed,
        "pending": pending
    }
