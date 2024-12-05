import sys
from app import create_app
from app.extensions import db
from app.models import User, Post, Comment

app = create_app()

def seed_database():
    alice = User(username="alice", email="alice@cerbosauthz.dev", is_admin=True, email_is_verified=True)
    alice.set_password("password123")

    andrew = User(username="andrew", email="andrew@cerbosauthz.dev", email_is_verified=True)
    andrew.set_password("password123")

    bob = User(username="bob", email="bob@cerbosauthz.dev")
    bob.set_password("password123")

    andrew_post_1 = Post(title="Andrew's First Published Post", body="This is Andrew's first published post.", is_published=True)
    andrew_post_2 = Post(title="Andrew's Second Published Post", body="This is Andrew's second published post.", is_published=True)
    andrew_post_3 = Post(title="Andrew's Third Published Post", body="This is Andrew's third published post.", is_published=True)
    andrew_post_4 = Post(title="Andrew's First Unpublished Post", body="This is Andrew's first unpublished post.", is_published=False)
    andrew_post_5 = Post(title="Andrew's Second Unpublished Post", body="This is Andrew's second unpublished post.", is_published=False)

    bob_post = Post(title="Bob's Published Post", body="This is Bob's only published post.", is_published=True)

    andrew.posts.extend([andrew_post_1, andrew_post_2, andrew_post_3, andrew_post_4, andrew_post_5])
    bob.posts.append(bob_post)

    comment_1 = Comment(body="This is Alice's first comment on Andrew's post.", user=alice, post=andrew_post_1)
    comment_2 = Comment(body="This is Alice's second comment on Andrew's post.", user=alice, post=andrew_post_1)

    db.session.add_all([alice, andrew, bob, comment_1, comment_2])

    try:
        db.session.commit()
        print("Database seeded successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while seeding the database: {e}")

if __name__ == "__main__":
    with app.app_context():
        seed_database()
