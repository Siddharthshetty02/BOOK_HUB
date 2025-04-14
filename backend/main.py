from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import uvicorn
from passlib.context import CryptContext
import os
from typing import Optional
# Initialize app
app = FastAPI()

# Security setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
def init_db():
    conn = sqlite3.connect("app.db", check_same_thread=False)
    cursor = conn.cursor()
    
    # Add link column if missing (safely handles existing columns)

    for column in ["rating", "progress"]:
        try:
            cursor.execute(f"ALTER TABLE books ADD COLUMN {column} INTEGER")
            conn.commit()
        except sqlite3.OperationalError:
            pass  # Column exists
    
    # Create tables if they don't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    
    # In init_db(), update the books table creation:
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        link TEXT,
        rating INTEGER CHECK (rating BETWEEN 1 AND 5),
        progress INTEGER CHECK (progress BETWEEN 0 AND 100),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
""")

    conn.commit()
    return conn, cursor

conn, cursor = init_db()

# Models
class User(BaseModel):
    username: str
    password: str
    
class Book(BaseModel):
    title: str
    author: str
    link: str = None  # New field for URLs
    rating: Optional[int] = None  # New (1-5)
    progress: Optional[int] = None  # New (0-100)
# Auth endpoints
@app.post("/register")
def register(user: User):
    try:
        hashed_password = pwd_context.hash(user.password)
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (user.username, hashed_password)
        )
        conn.commit()
        return {"message": "User created successfully"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")

@app.post("/login")
def login(user: User):
    cursor.execute(
        "SELECT id, password FROM users WHERE username = ?",
        (user.username,)
    )
    user_data = cursor.fetchone()
    
    if not user_data or not pwd_context.verify(user.password, user_data[1]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"message": "Login successful", "user_id": user_data[0]}

# Book endpoints
@app.post("/books")
def add_book(book: Book, user_id: int):
    cursor.execute(
        """INSERT INTO books 
        (title, author, user_id, link, rating, progress) 
        VALUES (?, ?, ?, ?, ?, ?)""",
        (book.title, book.author, user_id, book.link, book.rating, book.progress)
    )
    conn.commit()
    return {"message": "Book added", "id": cursor.lastrowid}

@app.get("/books")
def get_books(user_id: int):
    cursor.execute(
        "SELECT id, title, author, link FROM books WHERE user_id = ?",
        (user_id,)
    )
    return [{
        "id": row[0],
        "title": row[1], 
        "author": row[2],
        "link": row[3]  # Include the link in response
    } for row in cursor.fetchall()]
@app.put("/books/{book_id}")
def update_book(book_id: int, updates: dict, user_id: int):
    # Verify book belongs to user
    cursor.execute(
        "SELECT 1 FROM books WHERE id = ? AND user_id = ?",
        (book_id, user_id)
    )
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Build update query
    set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
    values = list(updates.values())
    
    cursor.execute(
        f"UPDATE books SET {set_clause} WHERE id = ?",
        (*values, book_id)
    )
    conn.commit()
    return {"message": "Book updated"}
if __name__ == "__main__":
    # Create database file if it doesn't exist
    if not os.path.exists("app.db"):
        init_db()
    uvicorn.run(app, host="0.0.0.0", port=8000)