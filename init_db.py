#!/usr/bin/env python3
"""Initialize the database and seed initial data"""
from app import create_app, db
from app.models import Tool, Category

def init_db():
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")

        # Ensure compatibility with older DBs: add category_id to tool if missing
        try:
            from sqlalchemy import inspect, text
            inspector = inspect(db.engine)
            cols = [c['name'] for c in inspector.get_columns('tool')]
            if 'category_id' not in cols:
                print("category_id column missing on 'tool' table; attempting to add it...")
                with db.engine.begin() as conn:
                    conn.execute(text('ALTER TABLE tool ADD COLUMN category_id INTEGER'))
                print("Added category_id column to 'tool' table.")
        except Exception as e:
            print('Compatibility step skipped or failed:', e)
            # continue — create_all will still have ensured Category table exists if possible

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

        # Ensure wp_db_compare tool exists (so it's visible in Manage Tools)
        if Tool.query.filter_by(name='wp_db_compare').count() == 0:
            wp_tool = Tool(
                name='wp_db_compare',
                display_name='WP SQL DB Compare',
                description='Compare two WordPress SQL dumps and produce a preview SQL patch.',
                icon='bi-database',
                route='/tools/wp-db-compare',
                is_active=True
            )
            db.session.add(wp_tool)
            db.session.commit()
            print('Seeded wp_db_compare tool')
        else:
            print('wp_db_compare tool already present')

        # Seed rule_card_formatter tool
        if Tool.query.filter_by(name='rule_card_formatter').count() == 0:
            rc_tool = Tool(
                name='rule_card_formatter',
                display_name='Rule Card Formatter',
                description='Format rule card text into bulleted or indented outputs.',
                icon='bi-list-ul',
                route='/tools/rule-card-formatter',
                is_active=True
            )
            db.session.add(rc_tool)
            db.session.commit()
            print('Seeded rule_card_formatter tool')
        else:
            print('rule_card_formatter tool already present')

        # Seed categories if not present
        if Category.query.count() == 0:
            general = Category(name='general', display_name='General')
            work = Category(name='work', display_name='Work')
            personal = Category(name='personal', display_name='Personal')
            home = Category(name='home', display_name='Home')
            db.session.add_all([general, work, personal, home])
            db.session.commit()
            # Add subcategory 'bkv' under work
            bkv = Category(name='bkv', display_name='BKV', parent_id=work.id)
            db.session.add(bkv)
            db.session.commit()
            print('Seeded default categories and subcategories')
        else:
            print('Categories already exist in database.')

if __name__ == '__main__':
    init_db()
