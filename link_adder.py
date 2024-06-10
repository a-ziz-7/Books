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
        "The 48 Laws of Power":["https://www.fop86.com/The%2048%20Laws%20of%20Power/The%2048%20Laws%20of%20Power%20-%20Robert%20Greene.pdf", "https://bjpcjp.github.io/pdfs/behavior/48-laws-power/The-48-Laws-of-Power-Robert-Greene.pdf"],
        "The Laws of Human Nature": ["https://irp-cdn.multiscreensite.com/cb9165b2/files/uploaded/The%20Laws%20of%20Human%20Nature.pdf"],
        "Influence": ["https://ia800203.us.archive.org/33/items/ThePsychologyOfPersuasion/The%20Psychology%20of%20Persuasion.pdf"],
        "Evolutionary Psychology (5th Edition)": ["https://www.researchgate.net/publication/325112371_Evolutionary_Psychology"],
        "Mans’ Search for Meaning": [],
        "How To Win Friends And Influence People": [],
        "Civilisation and Its Discontents": [],
        "Emotional Intelligence": [],
        "Learned Optimism": [],
        "The H Factor of Personality": [],
        "Blink": [],
        "Thinking Fast and Slow": [],
        "Riveted": [],
        "Psychology and You": [],
        "Curious": [],
        "Attached": [],
        "The Paradox of Choice": [],
        "Pre_Suasion": [],
        "Surrounded by idiots": [],
        "Made in America": [],
        "Memories, Dreams & Reflections": [],
        "Elon Musk": [],
        "The Everything Store": [],
        "Lord of The Flies": [],
        "Unbroken": [],
        "The Autobiography of Andrew Carnegie": [],
        "Shoe Dog": [],
        "Total Recall": [],
        "Michael Jordan The Life": [],
        "What You See Is What You Get": [],
        "Salt, Sugar, Fat": [],
        "Gut": [],
        "Poor Charlie’s Almanack": [],
        "Managing Oneself": [],
        "The Lessons of History": [],
        "PsychoCybernetics": [],
        "Mastery": [],
        "A Few Lessons For Managers And Investors": [],
        "Principles": [],
        "The Intelligent Investor": [],
        "The Art of War": [],
        "The 33 Strategies of War": [],
        "Thinking in Systems": [],
        "Small Move, Big Change": [],
        "The Selfish Gene": [],
        "The Hypomanic Edge": [],
        "Grit": [],
        "When": [],
        "The Art of Worldly Wisdom": [],
        "Deep Work": [],
        "The Law of Success": [],
        "Bounce": [],
        "Relentless": [],
        "Power vs Force": [],
        "The Power of Habit": [],
        "Discourses": [],
        "Letters from a Stoic": [],
        "The Shortness of Life": [],
        "Meditations": [],
        "Ego is The Enemy": [],
        "The Obstacle is The Way": [],
        "The Republic": [],
        "Eight Pillars of Prosperity": [],
        "Bookkeeping & Accounting for Dummies": [],
        "The innovators’ dilemma": [],
        "Excel 2016 for Dummies": [],
        "Zero to One": [],
        "Barbarians To Bureaucrats": [],
        "The Lean Startup": [],
        "Good To Great": [],
        "Ogilvy On Advertising": [],
        "Scientific Advertising": [],
        "Tested Advertising Methods": [],
        "Contagious": [],
        "How To Write A Good Advertisement": []    
    }
    for i in avaliabel_books:
        all_links = "||".join(avaliabel_books[i])
        insert_link(i, all_links)

conn.commit()
conn.close()