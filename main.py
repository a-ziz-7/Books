import sqlite3

file_path = "books.txt"
library = dict()
curr = ""

try:
    with open(file_path, "r") as file:
        contents = file.read()
        lines = contents.split("\n")
        for line in lines:
            result = line.split("-")
            if len(result) == 1:
                if result[0] == "":
                    continue
                library[result[0]] = []
                curr = result[0]
            else:
                library[curr].append((result[0].strip(), result[1].strip(), result[2].strip()))
except FileNotFoundError:
    print("File not found.")

# Connect to the database
conn = sqlite3.connect('library.sqlite')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()
# cursor.execute("DROP TABLE IF EXISTS genre")
# cursor.execute("DROP TABLE IF EXISTS authors")
# cursor.execute("DROP TABLE IF EXISTS books")
# cursor.execute("DROP TABLE IF EXISTS read_link")

# Create a table to store the books
cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS all_books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        bold BOOLEAN DEFAULT 0
    )
''')

# Create a table to store the genre
cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS genre (
        genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
        genre TEXT
    )
''')

# Create a table to store the authors
cursor.execute('''
    CREATE TABLE IF NOT EXISTS authors (
        author_id INTEGER PRIMARY KEY AUTOINCREMENT,
        a_first TEXT,
        a_last TEXT
    )
''')

# Create a table to store the books
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author_id INTEGER,
        genre_id INTEGER,
        bold BOOLEAN DEFAULT 0,
        FOREIGN KEY (author_id) REFERENCES authors(author_id),
        FOREIGN KEY (genre_id) REFERENCES genre(genre_id)
    )
''')

# Create a table to store the book links
cursor.execute('''
    CREATE TABLE IF NOT EXISTS read_link (
        read_id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        pdf_file TEXT,
        FOREIGN KEY (book_id) REFERENCES books(book_id)
    )
''')

def insert_genre(genre):
    cursor.execute('''
        INSERT INTO genre (genre)
        VALUES (?)
    ''', (genre,))

def chop(s):
    parts = s.split()
    if len(parts) == 1:
        return parts[0], ""
    else:
        return parts[0], " ".join(parts[1:])

def insert_author(author):
    f, l = chop(author)

    cursor.execute('''
        SELECT * FROM authors WHERE a_first = ? AND a_last = ?
    ''', (f, l))
    
    result = cursor.fetchone()
    if result is None:
        cursor.execute('''
            INSERT INTO authors (a_first, a_last)
            VALUES (?, ?)
        ''', (f, l))
        # print(f"Author '{author}' inserted successfully.")
    else:
        pass
        # print(f"Author '{author}' already exists.")
    # cursor.execute('''
    #     INSERT INTO authors (a_first, a_last)
    #     VALUES (?, ?)
    # ''', (f, l))

def insert_book(title, author, bold):
    cursor.execute('''
        INSERT INTO all_books (title, author, bold)
        VALUES (?, ?, ?)
    ''', (title, author, bold))

def insert_book(title, author, genre, bold):
    bold = True if bold == "1" else False
    f, l = chop(author)
    cursor.execute('''
        SELECT author_id FROM authors WHERE a_first = ? AND a_last = ?
    ''', (f, l))
    author_id = cursor.fetchone()[0]
    cursor.execute('''
        SELECT genre_id FROM genre WHERE genre = ?
    ''', (genre,))
    genre_id = cursor.fetchone()[0]
    
    cursor.execute('''
        INSERT INTO books (title, author_id, genre_id, bold)
        VALUES (?, ?, ?, ?)
    ''', (title, author_id, genre_id, bold))

def insert_read(book, pdf):
    cursor.execute('''
        SELECT book_id FROM books WHERE title = ?
    ''', (book,))
    book_id = cursor.fetchone()[0]
    cursor.execute('''
        INSERT INTO read_link (book_id, pdf_file)
        VALUES (?, ?)
    ''', (book_id, pdf))


for i in library:
    curr_arr = []
    # genre insertion
    # insert_genre(i)
    for book in library[i]:
        curr_arr.append(book)
    curr_arr.sort(key=lambda x: x[2], reverse=True)
    for book in curr_arr:
        # insert_author(book[1])
        # insert_book(book[0], book[1], i, book[2])
        pass
        
    # print("\n")


#Emanuel part

# insert_read("48 Laws of Power", "books/The 48 Laws of Power - Robert Greene.pdf")


# Commit the changes and close the connection
conn.commit()
conn.close()