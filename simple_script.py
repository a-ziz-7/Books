import sqlite3

conn = sqlite3.connect('library.sqlite')

cursor = conn.cursor()

cursor.execute("SELECT title FROM books")
all_books = cursor.fetchall()

for i in all_books:
    print(f"\"{i[0]}\": [],")