from flask import Flask, render_template, url_for
import sqlite3
import os

app = Flask(__name__)

def get_books_by_genre():
    conn = sqlite3.connect('library.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT genre.genre, books.title, books.bold
        FROM books
        JOIN genre ON books.genre_id = genre.genre_id
    ''')
    books_by_genre = cursor.fetchall()
    conn.close()

    library = {}
    for genre, title, bold in books_by_genre:
        if genre not in library:
            library[genre] = []
        library[genre].append((title, bold))
    return library

def get_book_details(title):
    conn = sqlite3.connect('library.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT books.title, authors.a_first, authors.a_last, genre.genre, books.bold
        FROM books
        JOIN authors ON books.author_id = authors.author_id
        JOIN genre ON books.genre_id = genre.genre_id
        WHERE books.title = ?
    ''', (title,))
    book_details = cursor.fetchone()
    conn.close()
    return book_details

@app.route('/')
def index():
    library = get_books_by_genre()
    return render_template('index.html', library=library)

@app.route('/book/<title>')
def book_detail(title):
    # Debugging: Print the title being accessed
    print(f"Accessing book detail for: {title}")
    book = get_book_details(title)
    return render_template('book_detail.html', book=book)

if __name__ == '__main__':
    # Print the template folder path
    # print(f"Template folder: {app.template_folder}")
    
    # Print the contents of the templates folder
    template_folder_path = app.template_folder
    if template_folder_path and os.path.exists(template_folder_path):
        print("Contents of the templates folder:")
        for root, dirs, files in os.walk(template_folder_path):
            for name in files:
                print(os.path.join(root, name))
    else:
        print("Templates folder not found.")
    
    app.run(debug=True)
