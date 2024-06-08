import sqlite3

conn = sqlite3.connect('library.sqlite')

cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS links")

cursor.execute('''
    CREATE TABLE IF NOT EXISTS links (
        link_id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        pdf_link TEXT,
        FOREIGN KEY (book_id) REFERENCES books(book_id)
    )
''')

def insert_link(book_title, pdf_link):
    cursor.execute('''
        SELECT book_id
        FROM books
        WHERE title = ?
    ''', (book_title,))
    book_id = cursor.fetchone()[0]
    cursor.execute('''
        INSERT INTO links (book_id, pdf_link)
        VALUES (?, ?)
    ''', (book_id, pdf_link))
    
    
if __name__ == '__main__':
    avaliabel_books = {
        "The 48 Laws of Power":["https://www.fop86.com/The%2048%20Laws%20of%20Power/The%2048%20Laws%20of%20Power%20-%20Robert%20Greene.pdf", "https://bjpcjp.github.io/pdfs/behavior/48-laws-power/The-48-Laws-of-Power-Robert-Greene.pdf"]
        
    }
    for i in avaliabel_books:
        all_links = "||".join(avaliabel_books[i])
        insert_link(i, all_links)

conn.commit()
conn.close()