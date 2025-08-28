from sqlalchemy.orm import Session
from .config import engine, SessionLocal
from .models import Base, SQLitePerson as Person, SQLiteSession as DBSession, SQLiteMessage as Message, SQLiteAISession as AISession
import uuid


def init_db():
    """Initialize the database with tables."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


def create_sample_data():
    """Create sample data for testing."""
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Person).first():
            print("Sample data already exists, skipping...")
            return
        
        # Create sample persons
        person1 = Person(
            full_name="John Doe",
            email_address="john.doe@example.com",
            phone_number="+1234567890"
        )
        
        person2 = Person(
            full_name="Jane Smith",
            email_address="jane.smith@example.com",
            phone_number="+1234567891"
        )
        
        db.add(person1)
        db.add(person2)
        db.commit()

        print("Person added successfully...")
        
        # Create a sample session
        session = DBSession(
            sender_id=str(person1.id),
            receiver_id=str(person2.id),
            subject="Initial project discussion and requirements gathering"
        )
        db.add(session)
        db.commit()

        print("Session added successfully...")
        
        # Create sample messages
        message1 = Message(
            session_id=str(session.session_id),
            sender_id=str(person1.id),
            receiver_id=str(person2.id),
            message_text="Hi Jane, I'd like to discuss the new project requirements. Can we schedule a meeting?",
            message_file=None,
            file_text=None        
        )
        
        message2 = Message(
            session_id=str(session.session_id),
            sender_id=str(person2.id),
            receiver_id=str(person1.id),
            message_text="Hi John, absolutely! I'm available tomorrow at 2 PM. Does that work for you?",
            message_file=None,
            file_text=None
        )
        
        db.add(message1)
        db.add(message2)
        db.commit()

        print("Message added successfully...")

        ai_session = AISession(
            esession_id=str(session.session_id)
        )

        db.add(ai_session)
        db.commit()

        print("AI session added successfully...")
        
        print("Sample data created successfully!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    create_sample_data() 