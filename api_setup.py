import sqlite3
import requests
from keys import key

def get_books_info(title, api_key):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        'q': title,
        'key': api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def fetch_titles_from_db(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT title FROM books")
    titles = [row[0] for row in cursor.fetchall()]
    connection.close()
    return titles

def insert_info(cursor, book_id, description, page_count, thumbnail, preview_link):
    cursor.execute('''
        INSERT INTO info (book_id, description, page_count, thumbnail, preview_link)
        VALUES (?, ?, ?, ?, ?)
    ''', (book_id, description, page_count, thumbnail, preview_link))

def main():
    conn = sqlite3.connect('library.sqlite')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS info")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            description TEXT,
            page_count INTEGER,
            thumbnail TEXT,
            preview_link TEXT,
            FOREIGN KEY (book_id) REFERENCES genre(book_id)
        )
    ''')
    api_key = key
    db_path = 'library.sqlite'

    # Fetch titles from the database
    titles = fetch_titles_from_db(db_path)
    i = 1
    for title in titles[:]:
        try:
            books_data = get_books_info(title, api_key)
            for item in books_data.get('items', []):
                volume_info = item.get('volumeInfo', {})
                title = volume_info.get('title', 'No title')
                authors = volume_info.get('authors', 'No authors')
                description = volume_info.get('description', 'No description')
                page_count = volume_info.get('pageCount', 'No page count')
                thumbnail = volume_info.get('imageLinks', {}).get('thumbnail', 'No thumbnail')
                preview_link = volume_info.get('previewLink', 'No preview link')

                print(f'Title: {title}')
                print(f'Authors: {authors}')
                print(f'Description: {description[:70]}')
                print(f'Page Count: {page_count}')
                print(f'Thumbnail: {thumbnail}')
                print(f'Preview Link: {preview_link}')
                print('-' * 40)
                insert_info(cursor, i, description, page_count, thumbnail, preview_link)
                i += 1
                break
        except requests.exceptions.RequestException as e:
            print(f'Error fetching data for title "{title}": {e}')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
