import sqlite3

connection = sqlite3.connect("tasks.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    done BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
   """)
   

cursor.execute("SELECT COUNT(*) FROM tasks")
count = cursor.fetchone()[0]

if count == 0:
    cursor.executemany(
    "INSERT INTO tasks(title, done) VALUES (?, ?)",
    [
        ("Learn FastAPI", False),
        ("Learn SQLite",True),
        ("Build Todo API", False),
    ]
)

connection.commit()

def get_all_tasks(search=None, done=None):
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    query = "SELECT * FROM tasks"
    
    params = []

    if search:
        query += " WHERE title LIKE ?"
        params.append(f"%{search}%")

    elif done is not None:
        query += " WHERE done = ?"
        params.append(done)

    query += " ORDER BY title ASC"

    cursor.execute(query, params)
        
    rows = cursor.fetchall()

    connection.close()
    return rows
    # connection.commit()


def get_by_id(task_id:int):
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks where id = ? ",(task_id,))
    rows = cursor.fetchone()
    connection.close()
    return rows
    # connection.commit()


def add_task(title: str, done=bool):
   
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    
    cursor.execute("INSERT INTO tasks(title,done) VALUES(?,?)",(title,done))
    cursor.execute(
    "SELECT * FROM tasks WHERE id = last_insert_rowid()")
    task = cursor.fetchone()
    
    
    connection.commit()
    
    connection.close()
    return task


def update_task(id: int, title: str, done: bool):
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE tasks
        SET title = ?, done = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (title, done, id))

    connection.commit()

    cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
    updated_task = cursor.fetchone()

    connection.close()

    return updated_task

def delete_task(id:int):
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    cursor.execute("DELETE from tasks WHERE id=?",(id,))
    connection.commit()
    deleted = cursor.rowcount

    connection.close()
    return deleted 

def get_stats():
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE done = 1")
    completed = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE done = 0")
    pending = cursor.fetchone()[0]

    connection.close()

    return {
        "total": total,
        "completed": completed,
        "pending": pending
    }
connection.close()