# Gebeya API

Gebeya API is a Django REST Framework backend for a marketplace-style application with products, accounts, chat, wishlist, reports, and admin features.

## Features

- User authentication and JWT-based auth
- Product management and categories
- Favorites and product views tracking
- Chat support
- Admin endpoints

## Tech Stack

- Python 3.11
- Django 6.0.5
- Django REST Framework
- SQLite (default)
- Docker support

## Project Structure

- apps/accounts - authentication and user-related logic
- apps/products - products, categories, favorites, and views
- apps/chat - real-time chat functionality
- apps/wishlist - wishlist management
- apps/reports - reporting features
- apps/adminapp - admin-specific endpoints
- config - Django project settings and URL routing

## Setup

### 1. Create and activate a virtual environment

```bash
python -m venv env
source env/bin/activate
```

On Windows:

```bash
env\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Apply migrations

```bash
python manage.py migrate
```

### 4. Run the development server

```bash
python manage.py runserver
```

## Docker

Build and run with Docker Compose:

```bash
docker compose up --build
```

The app will be available at:

```text
http://localhost:8000
```

## Useful Commands

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py test
```

## Notes

- The project currently uses SQLite for local development.
- Media files are stored under the media directory.
