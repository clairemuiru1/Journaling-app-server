from app import app, db
from models import User, JournalEntry
 
def seed():
    # Create users
    user3 = User(
        firstname="paul",
        lastname="Doe",
        username="pauldoe",
        email="paul@example.com",
    )
    user3.password_hash = "password12345"  # This will be hashed by the password_hash setter
 
    user4 = User(
        firstname="Jane",
        lastname="Smith",
        username="janesmith",
        email="jane@example.com",
    )
    user4.password_hash = "password123"  # This will be hashed by the password_hash setter
 
    db.session.add(user3)
    db.session.add(user4)
    db.session.commit()
 
    # Create journal entries
    entry1 = JournalEntry(
        title="My First Entry",
        content="This is the content of my first journal entry.",
        category="Personal",
        user_id=user3.id
    )
    entry2 = JournalEntry(
        title="Work Update",
        content="Today I made significant progress at work.",
        category="Work",
        user_id=user3.id
    )
    entry3 = JournalEntry(
        title="Travel Plans",
        content="Planning a trip to Europe next summer.",
        category="Travel",
        user_id=user4.id
    )
 
    db.session.add(entry1)
    db.session.add(entry2)
    db.session.add(entry3)
    db.session.commit()
 
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed()
        print("Database seeded!")
 