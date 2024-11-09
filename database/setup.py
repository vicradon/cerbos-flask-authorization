import sqlite3
import random
import os
from database import Database  
from dotenv import load_dotenv

load_dotenv()
db_path = os.getenv('DB_PATH')

def initialize_db(db: Database):
    try:
        connection = sqlite3.connect(db.db_path) 
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                is_admin BOOLEAN DEFAULT FALSE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                FOREIGN KEY (post_id) REFERENCES posts (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        connection.commit()
        print("Database initialized.")
    except Exception as error:
        print(f"Error initializing database: {error}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def seed_data(db: Database):
    try:
        connection = sqlite3.connect(db.db_path)  
        cursor = connection.cursor()
        
        users = [
            ("Alice", "Smith", "ASmith", "incorrect", True),   
            ("Bob", "Jones", "BJ", "passwors-suck", False),
            ("Charlie", "Brown", "cJBrown", "test-1234", False),
            ("Diana", "Prince", "DiaSama", "milk-and-shakes", False),
            ("Eve", "Johnson", "EvoJojo", "apples-and-pies", False)
        ]
        cursor.executemany("INSERT INTO users (first_name, last_name, username, password, is_admin) VALUES (?, ?, ?, ?, ?)", users)
        connection.commit()
        print(f"{cursor.rowcount} users inserted.")

        cursor.execute("SELECT id FROM users WHERE is_admin = 0")
        non_admin_users = [row[0] for row in cursor.fetchall()]

        titles = ["Exploring", "Understanding", "The Art of", "A Guide to", "Top Tips for", "Insights on"]
        topics = ["coding", "mindfulness", "productivity", "art", "technology", "travel", "recipes"]
        content_starters = [
            "In this post, we'll dive into the nuances of",
            "Here are some effective ways to approach",
            "Let's explore how to make the most of",
            "A comprehensive guide on",
            "Thoughts on the importance of",
            "Today, we’ll examine"
        ]
        additional_sentences = [
            "This topic has a profound impact on various aspects of our daily lives.",
            "Many people find this subject to be both challenging and rewarding.",
            "It's essential to understand the basics before diving deeper.",
            "Let's break down some key principles and actionable steps.",
            "Consider these insights as you work on improving your understanding.",
            "The following tips can help you get started in the right direction."
        ]
        comment_phrases = [
            "Great insights on this topic!", "I totally agree with your points.",
            "Thanks for sharing your thoughts!", "This was really informative and helpful.",
            "I learned a lot from this post!", "Interesting perspective on the subject.",
            "Looking forward to more posts like this!", "Well explained!",
            "This really resonates with my experiences.", "I appreciate the detailed breakdown.",
            "I’ve been struggling with this, and this post really helped!",
            "Some really valuable tips here—thank you!"
        ]

        post_count = 0
        for user_id in non_admin_users:
            num_posts = random.randint(5, 8)
            posts = []
            for _ in range(num_posts):
                title = f"{random.choice(titles)} {random.choice(topics)}"
                content = (
                    f"{random.choice(content_starters)} {random.choice(topics)}. "
                    f"{random.choice(additional_sentences)} "
                    f"{random.choice(additional_sentences)}"
                )
                posts.append((user_id, title, content))
            cursor.executemany("INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)", posts)
            post_count += cursor.rowcount
        connection.commit()
        print(f"{post_count} posts inserted.")

        cursor.execute("SELECT id FROM posts")
        all_posts = [row[0] for row in cursor.fetchall()]

        comment_count = 0
        cursor.execute("SELECT id FROM users")
        all_users = [row[0] for row in cursor.fetchall()]

        comments = []
        for post_id in all_posts:
            num_comments = random.randint(1, 5)
            for _ in range(num_comments):
                user_id = random.choice(all_users)
                content = random.choice(comment_phrases)
                comments.append((post_id, user_id, content))
        cursor.executemany("INSERT INTO comments (post_id, user_id, content) VALUES (?, ?, ?)", comments)
        connection.commit()
        comment_count += cursor.rowcount
        print(f"{comment_count} comments inserted.")

    except Exception as error:
        print(f"Error seeding data: {error}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


if __name__ == "__main__":
    db = Database()
    
    initialize_db(db)
    seed_data(db) 