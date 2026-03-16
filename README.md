# week8-flask-blog
A full‑stack personal blog web application built with Flask, showcasing routing, templates, authentication, databases, and CRUD operations. This project demonstrates end‑to‑end web development skills with Python and Flask.

## Project Description
Personal Blog with Flask is a feature‑complete blogging platform that allows users to:
- Register and log in securely.
- Create, edit, and delete blog posts.
- Comment on posts and optionally moderate comments.
- Browse posts with pagination, categories, and search.
The application uses Flask, SQLAlchemy, Jinja2 templates, and Bootstrap to demonstrate how to build a real-world web application with Python.

## Learning
1. Web frameworks and Flask basics
  - How web frameworks simplify HTTP handling and routing.
  - Setting up a Flask project with the application factory pattern and blueprints.
2. Routing and views
  - Mapping URLs to view functions using Flask routes.
  - Organizing routes across multiple blueprints (auth, main, posts, comments).
3. Templates and Jinja2
  - Using Jinja2 to render dynamic HTML.
  - Template inheritance with base.html and block overrides.
  - Control structures in templates (loops, conditionals).
3. Forms and user input
  - Building forms with Flask-WTF / WTForms.
  - Handling POST requests, validation, and displaying error messages.
  - CSRF protection.
4. Static files and frontend
  - Serving CSS, JavaScript, and images from static/.
  - Using Bootstrap for responsive design and a modern layout.
5. Authentication and authorization
  - Implementing user registration, login, logout using Flask‑Login.
  - Securing routes with @login_required.
  - Hashing passwords using Werkzeug.
6. Persistence and data modeling
  - Designing database models for users, posts, and comments.
  - Using SQLAlchemy for ORM and relationships.
  - Managing schema changes with Flask‑Migrate (Alembic).
7. Testing and deployment basics
  - Writing basic tests for models and views.
  - Running the app in a local development environment with the Flask dev server.

## Architecture
1. Application Factory (app/__init__.py)
- Creates and configures the Flask application via create_app(config_class=Config).
- Initializes extensions:
  - SQLAlchemy (database access)
  - Flask-Migrate (schema migrations)
  - Flask-Login (user session management)
  - Flask-Bootstrap (Bootstrap integration)
- Registers blueprints:
  - auth: authentication routes (/auth/...)
  - main: home page, profile, general views
  - posts: post CRUD operations (/posts/...)
  - comments: comment endpoints (/comments/...)
- Adds error handlers for 404 and 500 pages.
- Exposes shell context for flask shell (e.g. db, User, Post, Comment).

2. Models (app/models.py)
- User:
  - Fields: id, username, email, password_hash, about_me, member_since, last_seen.
  - Relationships: posts, comments.
  - Methods: set_password, check_password.
- Post:
  - Fields: id, title, content, timestamp, updated_at, published, user_id.
  - Relationship: comments (cascade delete).
- Comment:
  - Fields: id, content, timestamp, approved, user_id, post_id.

## Features
1. User Authentication
- Register new users with unique username & email.
- Log in/log out using secure sessions.
- Password hashing and safe storage.
2. Blog Post Management (CRUD)
- Create new blog posts with title and rich content.
- Edit and delete existing posts (author‑only).
- List posts on home page and individual post detail views.
- Pagination for large numbers of posts.
- Optional search and filtering.
3. Comment System
- Add comments to posts as authenticated users.
- Display comments under each post.
- Basic moderation via approved flag; only approved comments show publicly.
- Optionally extendable to nested replies.

4. Frontend & Layout
- Jinja2 templates with a common base.html.
- Responsive design using Bootstrap.
- Navigation bar with links to Home, Posts, Login/Register, Profile.
- Optional components: rich text editor for posts, search bar, tag badges.
5. Static Assets
- Centralized static/ folder for CSS, JS, and images.
- Custom styling layered on top of Bootstrap.
6. Database & Migrations
- SQLite database for local development.
- Managed through SQLAlchemy and Flask-Migrate.

## How to Run
From the week8-flask-blog/ root:
python -m venv .venv
pip install -r requirements.txt

## Initialize the Database
Initialize migrations (first time only)
flask db init         # if not already present
flask db migrate -m "Initial migration"
flask db upgrade

## Run the Application
python run.py

using Flask CLI:

export FLASK_APP=run.py       
export FLASK_ENV=development   
flask run

