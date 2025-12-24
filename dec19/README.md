# Simple Django Shop

This project is a minimal Django shop with two apps:

- `store`: categories and products (CRUD).
- `users`: user management (CRUD using Django's User model).

All templates extend `base.html`.

Quick start:

1. Create a virtualenv and install requirements:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run migrations and start server:

```bash
python manage.py migrate
python manage.py createsuperuser  # optional
python manage.py runserver
```

Home page shows recommended products. Product detail pages show links to category and the creating user; those links list products by category or user.
