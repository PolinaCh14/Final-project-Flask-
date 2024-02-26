import sqlite3

connection = sqlite3.connect("database.db")

data = [("Main post",), ("Post",), ("Friend",)]

with open("schema.sql") as f:
    connection.executescript(f.read())

cur = connection.cursor()
cur.execute(
    "INSERT INTO type (type) VALUES (?)",
    ("Main post",),
)
cur.execute(
    "INSERT INTO type (type) VALUES (?)",
    ("Post",),
)
cur.execute(
    "INSERT INTO type (type) VALUES (?)",
    ("Friend",),
)

cur.execute(
    "INSERT INTO posts (title, content, photo, photo_name, type_id) VALUES (?, ?, ?, ?, ?)",
    (
        "About main post",
        "Content for the first post, text fkfjkdjfd",
        "https://i.pinimg.com/236x/d5/f7/c0/d5f7c0eb835e316f9119fc151414fd31.jpg",
        "sjsjsjjsksjskjs",
        1,
    ),
)

cur.execute(
    "INSERT INTO posts (title, content, photo, photo_name, type_id) VALUES (?, ?, ?, ?, ?)",
    (
        "First Post",
        "Content for the first post",
        "https://i.pinimg.com/236x/d5/f7/c0/d5f7c0eb835e316f9119fc151414fd31.jpg",
        "sjsjsjjsksjskjs",
        2,
    ),
)

cur.execute(
    "INSERT INTO posts (title, content, photo, photo_name, type_id) VALUES (?, ?, ?, ?, ?)",
    (
        "Second Post",
        "Content for the second post",
        "https://i.pinimg.com/736x/39/22/14/392214bc2aa4c85c3e7fc4f0515dc59c.jpg",
        "Second photo",
        2,
    ),
)

cur.execute(
    "INSERT INTO posts (title, content, photo, photo_name, type_id) VALUES (?, ?, ?, ?, ?)",
    (
        "Fffffff Post",
        "Content for the ffffffff post",
        "https://i.pinimg.com/564x/66/87/1a/66871a3bc082c08a2fd56dea5bf3d1f5.jpg",
        "Ffffff photo",
        3,
    ),
)

connection.commit()
connection.close()
