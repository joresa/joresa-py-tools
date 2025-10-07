#!/usr/bin/env python3
"""Initialize the database and seed initial data"""
from app import create_app, db
from app.models import Tool

def init_db():
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Check if tools already exist
        if Tool.query.count() == 0:
            # Seed initial tools
            tools = [
                Tool(
                    name='diff_checker',
                    display_name='Diff Checker',
                    description='Compare two texts or files and see highlighted changes with complete history tracking.',
                    icon='bi-file-earmark-diff',
                    route='/tools/diff',
                    is_active=True
                ),
            ]
            
            for tool in tools:
                db.session.add(tool)
            
            db.session.commit()
            print(f"Seeded {len(tools)} tool(s) into database!")
        else:
            print("Tools already exist in database.")

if __name__ == '__main__':
    init_db()
