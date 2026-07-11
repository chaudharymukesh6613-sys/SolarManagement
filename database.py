import sqlite3

def connect_db():
    return sqlite3.connect("solar.db")


conn = connect_db()
cur = conn.cursor()

# Customer Table
cur.execute("""
CREATE TABLE IF NOT EXISTS customers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    mobile TEXT NOT NULL,
    email TEXT NOT NULL,
    address TEXT,
    panel TEXT
)
""")

# Solar Panel Table
cur.execute("""
CREATE TABLE IF NOT EXISTS panels(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    panel_name TEXT NOT NULL,
    company TEXT NOT NULL,
    watt INTEGER,
    price REAL,
    stock INTEGER
)
""")

# Installation Table
cur.execute("""
CREATE TABLE IF NOT EXISTS installations(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    install_date TEXT,
    technician TEXT,
    status TEXT
)
""")

# Billing Table
cur.execute("""
CREATE TABLE IF NOT EXISTS bills(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bill_no TEXT,
    customer_name TEXT,
    amount REAL,
    gst REAL,
    total REAL
)
""")

conn.commit()
conn.close()

print("Database Created Successfully.")