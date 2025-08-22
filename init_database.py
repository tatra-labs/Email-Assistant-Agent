#!/usr/bin/env python3
"""
Database initialization script for Email Assistant Agent.
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from email_assistant.backend.database.config import engine
from email_assistant.backend.database.models import Base
from email_assistant.backend.database.init_db import init_db, create_sample_data


def main():
    """Initialize the database."""
    print("Initializing Email Assistant Agent database...")
    
    try:
        # Create tables
        init_db()
        
        # Create sample data
        create_sample_data()
        
        print("Database initialization completed successfully!")
        print("Database file: email_assistant.db")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 