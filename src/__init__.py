import sqlite3
import hashlib
import os

class Database:
    def __init__(self, db_path="data/stock.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.create_tables()
        
    def create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Tabla de usuarios
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL
                )
            """)
            # Tabla de artículos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    sku TEXT UNIQUE NOT NULL,
                    price REAL NOT NULL,
                    quantity INTEGER NOT NULL,
                    location TEXT NOT NULL
                )
            """)
            # Crear usuario por defecto (admin/admin123)
            default_user = "admin"
            default_pass = hashlib.sha256("admin123".encode()).hexdigest()
            cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", 
                         (default_user, default_pass))
            conn.commit()

    def verify_user(self, username, password):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            if result:
                stored_password = result[0]
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                return stored_password == hashed_password
            return False

    def add_user(self, username, password):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                             (username, hashed_password))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False  # Usuario ya existe

    def add_item(self, name, sku, price, quantity, location):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO items (name, sku, price, quantity, location) 
                    VALUES (?, ?, ?, ?, ?)
                """, (name, sku, price, quantity, location))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False  # SKU ya existe

    def get_all_items(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, sku, price, quantity, location FROM items")
            return cursor.fetchall()

    def update_item(self, id, name, sku, price, quantity, location):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    UPDATE items SET name = ?, sku = ?, price = ?, quantity = ?, location = ?
                    WHERE id = ?
                """, (name, sku, price, quantity, location, id))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    def delete_item(self, id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM items WHERE id = ?", (id,))
            conn.commit()