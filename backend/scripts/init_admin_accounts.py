"""
Initialize admin accounts for MediFlow OS
Creates four admin accounts for different departments
"""

import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.append(str(Path(__file__).parent.parent))

from database.connection import SessionLocal, init_db
from crud import admin_user as admin_crud
from crud import department_chat as chat_crud


def seed_admin_accounts():
    """Create the four admin accounts"""
    db = SessionLocal()
    
    try:
        # Define the four admin accounts
        admin_accounts = [
            {"username": "pharmacy_admin", "department": "Pharmacy"},
            {"username": "radiology_admin", "department": "Radiology"},
            {"username": "general_ward_admin", "department": "General Ward"},
            {"username": "administration_admin", "department": "Administration"},
        ]
        
        print("🔧 Creating admin accounts...")
        
        for account in admin_accounts:
            # Check if account already exists
            existing = admin_crud.get_by_username(db, account["username"])
            if existing:
                print(f"  ⚠️  {account['username']} already exists, skipping...")
                continue
            
            # Create the account
            admin = admin_crud.create(db, account["username"], account["department"])
            print(f"  ✅ Created {admin.username} for {admin.department}")
        
        print("\n💬 Adding sample chat messages...")
        
        # Add some sample messages for each department
        sample_messages = [
            {
                "department": "Pharmacy",
                "sender_username": "pharmacy_admin",
                "message_text": "Restocking antibiotics in 30 mins."
            },
            {
                "department": "Radiology",
                "sender_username": "radiology_admin",
                "message_text": "CT scan backlog cleared, ready for new slots."
            },
            {
                "department": "General Ward",
                "sender_username": "general_ward_admin",
                "message_text": "Two beds freed in ward B2."
            },
            {
                "department": "Administration",
                "sender_username": "administration_admin",
                "message_text": "Monthly reports due by end of week."
            },
        ]
        
        for msg in sample_messages:
            chat_crud.create_message(
                db,
                msg["department"],
                msg["sender_username"],
                msg["message_text"]
            )
            print(f"  ✅ Added message to {msg['department']}")
        
        print("\n✨ Admin accounts and sample messages created successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("MediFlow OS - Admin Account Initialization")
    print("=" * 60)
    print()
    
    # Initialize database tables first
    print("📊 Initializing database tables...")
    init_db()
    print()
    
    # Seed admin accounts
    seed_admin_accounts()
    
    print()
    print("=" * 60)
    print("✅ Initialization complete!")
    print("=" * 60)


# Made with Bob