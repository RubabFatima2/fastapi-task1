import sqlite3

connection = sqlite3.connect("tasks.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    done BOOLEAN)
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

def get_all_tasks():
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks")

    rows = cursor.fetchall()
    return rows
    connection.close()
    # connection.commit()


def get_by_id(task_id:int):
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks where id = ? ",(task_id,))
    rows = cursor.fetchone()
    connection.close()
    return rows
    # connection.commit()


def add_task(title: str):
   
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    done = False
    cursor.execute("INSERT INTO tasks(title,done) VALUES(?,?)",(title,done))
    cursor.execute(
    "SELECT * FROM tasks WHERE id = last_insert_rowid()")
    task = cursor.fetchone()
    
    
    connection.commit()
    connection.close()
    return task
connection.close()