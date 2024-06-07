import requests
from keys import key

def get_books(query, api_key):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        'q': query,
        'key': api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        # print(response.json())
        return response.json()
    else:
        response.raise_for_status()

# Replace 'YOUR_API_KEY' with your actual Google Books API key
api_key = key

# Example search query
query = 'The 48 Laws of Power'

# Get books data
try:
    books_data = get_books(query, api_key)
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
        print(f'Description: {description[:50]}')
        print(f'Page Count: {page_count}')
        print(f'Thumbnail: {thumbnail}')
        print(f'Preview Link: {preview_link}')
        print('-' * 40)
        break

except requests.exceptions.RequestException as e:
    print(f'Error: {e}')
