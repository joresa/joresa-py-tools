from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.tools import bp as tools_bp
    app.register_blueprint(tools_bp, url_prefix='/tools')

    with app.app_context():
        db.create_all()

    @app.context_processor
    def inject_categories():
        # Provide categories and their tools for navigation
        try:
            from app.models import Category, Tool
            from sqlalchemy import func
            from sqlalchemy.orm import selectinload
            # Only top-level categories (parent_id is NULL), eager-load children and tools
            cats = Category.query.options(selectinload(Category.children), selectinload(Category.tools))\
                .filter(Category.parent_id == None)\
                .order_by(func.lower(func.coalesce(Category.display_name, Category.name)))\
                .all()
            # Filter out categories that have no tools and whose children also have no tools
            visible = []
            for c in cats:
                has_tools = bool(c.tools)
                has_child_tools = any(bool(child.tools) for child in c.children)
                if has_tools or has_child_tools:
                    visible.append(c)

            # Also expose unassigned tools (helpful so users can assign a category from Manage Tools and access the tool immediately)
            unassigned_tools = Tool.query.filter(Tool.category_id == None, Tool.is_active == True).order_by(func.lower(func.coalesce(Tool.display_name, Tool.name))).all()

            return {'nav_categories': visible, 'nav_unassigned_tools': unassigned_tools}
        except Exception:
            return {'nav_categories': [], 'nav_unassigned_tools': []}

    return app

from app import models
