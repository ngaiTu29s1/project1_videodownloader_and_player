import sqlite3
import os
import requests
import time
from core.constants import OMDB_API_KEY, OMDB_API_URL


# Ensure the db folder exists
DB_FOLDER = os.path.join("core", "db")
os.makedirs(DB_FOLDER, exist_ok=True)

ACCOUNT_DB_FILE = os.path.join(DB_FOLDER, "account.db")
MOVIE_DB_FILE = os.path.join(DB_FOLDER, "movie.db")

def create_account_connection():
    return sqlite3.connect(ACCOUNT_DB_FILE)

def create_movie_connection():
    return sqlite3.connect(MOVIE_DB_FILE)

# Account management functions
def create_account_table():
    conn = create_account_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_account(username, password, email):
    conn = create_account_connection()
    cursor = conn.cursor()
    try:
        # Check if username already exists
        cursor.execute("SELECT id FROM accounts WHERE username = ?", (username,))
        if cursor.fetchone():
            print(f"Username '{username}' already exists.")
        else:
            cursor.execute("""
                INSERT INTO accounts (username, password, email)
                VALUES (?, ?, ?)
            """, (username, password, email))  # Store password as plain text
            conn.commit()
            print(f"Account '{username}' created.")
    except sqlite3.IntegrityError:
        print(f"Username '{username}' already exists.")
    conn.close()

def list_accounts():
    conn = create_account_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email FROM accounts")
    accounts = cursor.fetchall()
    conn.close()
    return accounts

# Movie database functions
def create_movie_table():
    conn = create_movie_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year TEXT,
            rated TEXT,
            released TEXT,
            runtime TEXT,
            genre TEXT,
            director TEXT,
            writer TEXT,
            actors TEXT,
            plot TEXT,
            language TEXT,
            country TEXT,
            awards TEXT,
            poster TEXT,
            imdb_rating TEXT,
            imdb_votes TEXT,
            imdb_id TEXT UNIQUE,
            type TEXT,
            box_office TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_movie(movie):
    conn = create_movie_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO movies (
            title, year, rated, released, runtime, genre, director, writer, actors, plot,
            language, country, awards, poster, imdb_rating, imdb_votes, imdb_id, type, box_office
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        movie.get("Title"),
        movie.get("Year"),
        movie.get("Rated"),
        movie.get("Released"),
        movie.get("Runtime"),
        movie.get("Genre"),
        movie.get("Director"),
        movie.get("Writer"),
        movie.get("Actors"),
        movie.get("Plot"),
        movie.get("Language"),
        movie.get("Country"),
        movie.get("Awards"),
        movie.get("Poster"),
        movie.get("imdbRating"),
        movie.get("imdbVotes"),
        movie.get("imdbID"),
        movie.get("Type"),
        movie.get("BoxOffice"),
    ))
    conn.commit()
    conn.close()

def fetch_and_store_20_movies():
    api_key = OMDB_API_KEY
    url = OMDB_API_URL
    movie_titles = [
        "The Shawshank Redemption", "The Godfather", "The Dark Knight", "Pulp Fiction",
        "Forrest Gump", "Inception", "Fight Club", "The Matrix", "Goodfellas", "Se7en",
        "The Silence of the Lambs", "Interstellar", "The Green Mile", "Gladiator",
        "Saving Private Ryan", "The Prestige", "The Lion King", "The Departed",
        "Whiplash", "The Intouchables", "The Pianist", "Parasite", "Joker",
        "Avengers: Endgame", "WALL·E", "Coco", "Braveheart", "Memento", "Alien",
        "Oldboy", "The Shining", "Django Unchained", "The Wolf of Wall Street",
        "Shutter Island", "The Truman Show", "A Beautiful Mind", "The Grand Budapest Hotel",
        "No Country for Old Men", "Blade Runner 2049", "La La Land", "Logan",
        "Mad Max: Fury Road", "Her", "Inside Out", "Up", "Toy Story", "Finding Nemo",
        "Monsters, Inc.", "Ratatouille", "The Incredibles", "Spirited Away",
        "Princess Mononoke", "My Neighbor Totoro", "Howl's Moving Castle", "Your Name",
        "Grave of the Fireflies", "Akira", "Ghost in the Shell", "The Iron Giant",
        "Big Hero 6", "Zootopia", "Frozen", "Moana", "Tangled", "Aladdin", "Beauty and the Beast",
        "The Little Mermaid", "Cinderella", "Snow White and the Seven Dwarfs",
        "Sleeping Beauty", "Bambi", "Pinocchio", "Peter Pan", "Lady and the Tramp",
        "101 Dalmatians", "The Jungle Book", "Robin Hood", "The Aristocats",
        "The Rescuers", "The Fox and the Hound", "The Black Cauldron", "The Great Mouse Detective",
        "Oliver & Company", "The Hunchback of Notre Dame", "Hercules", "Mulan",
        "Tarzan", "The Emperor's New Groove", "Atlantis: The Lost Empire",
        "Lilo & Stitch", "Treasure Planet", "Brother Bear", "Home on the Range",
        "Chicken Little", "Meet the Robinsons", "Bolt", "The Princess and the Frog"
    ]
    # Get already stored imdbIDs to avoid duplicates
    conn = create_movie_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT imdb_id FROM movies")
    existing_ids = set(row[0] for row in cursor.fetchall())
    conn.close()

    # Filter out titles already in database
    available_titles = []
    for title in movie_titles:
        params = {"t": title, "apikey": api_key}
        try:
            res = requests.get(url, params=params, timeout=10)
            data = res.json()
            imdb_id = data.get("imdbID")
            if data.get("Response") == "True" and imdb_id and imdb_id not in existing_ids:
                available_titles.append(title)
            time.sleep(0.1)
        except Exception:
            continue
        if len(available_titles) >= 20:
            break

    if not available_titles:
        print("No new movies to add.")
        return

    print(f"Fetching and storing {len(available_titles)} new movies...")
    for idx, title in enumerate(available_titles, 1):
        params = {"t": title, "apikey": api_key}
        try:
            res = requests.get(url, params=params, timeout=10)
            data = res.json()
            if data.get("Response") == "True":
                insert_movie(data)
                print(f"{idx} - {data.get('Title')} | Inserted")
            else:
                print(f"{idx} - {title} | Not found")
        except Exception as e:
            print(f"{idx} - {title} | Error: {e}")
        time.sleep(0.2)

def print_all_accounts():
    conn = create_account_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(accounts)")
    columns = [col[1] for col in cursor.fetchall()]
    cursor.execute("SELECT * FROM accounts")
    rows = cursor.fetchall()
    conn.close()
    print("Accounts:")
    print(columns)
    for row in rows:
        print(row)

def print_all_movies():
    conn = create_movie_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(movies)")
    columns = [col[1] for col in cursor.fetchall()]
    cursor.execute("SELECT * FROM movies")
    rows = cursor.fetchall()
    conn.close()
    print("Movies:")
    print(columns)
    for row in rows:
        print(row)

if __name__ == "__main__":
    create_account_table()
    create_movie_table()
    # Example data
    # insert_account("alice", "password123", "alice@example.com")
    # insert_account("bob", "securepass", "bob@example.com")
    # print(list_accounts())
    # Fetch and store 20 movies (no duplicates)
    # fetch_and_store_20_movies()
    # print_all_movies()
    # print_all_accounts()

