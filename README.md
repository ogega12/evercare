Garage Website — Evercare Garage

Overview
--------
A professional garage/automotive marketing website built with Django, Bootstrap 5, and modern web practices. Responsive, production-ready, and ready to connect to PostgreSQL.

Features
--------
- Django backend with admin
- Bootstrap 5 frontend (mobile-first)
- Services managed via Django admin
- Booking & contact forms saved to DB
- Image upload for services, gallery, promotions, testimonials
- WhatsApp quick contact
- Google Maps integration
- SEO-friendly structure

Quick setup (Windows)
---------------------
Open PowerShell and run:

1) Create and activate virtual env
python -m venv venv
venv\Scripts\Activate.ps1   # or venv\Scripts\activate for cmd.exe

2) Install dependencies
pip install -r requirements.txt

3) Create .env from .env.example and set values
copy .env.example .env
# Edit .env with your preferred editor and set SECRET_KEY and DATABASE_URL

4) Apply migrations
python manage.py makemigrations
python manage.py migrate

5) Create superuser
python manage.py createsuperuser

6) Run development server
python manage.py runserver

7) Collect static for production
python manage.py collectstatic --noinput

Production notes
----------------
- Copy `.env.example` to `.env` and set a long, unique `SECRET_KEY`, `DEBUG=False`,
  `ALLOWED_HOSTS`, and `CSRF_TRUSTED_ORIGINS`.
- Use PostgreSQL in production via `DATABASE_URL`; run `python manage.py migrate`
  during deployment.
- Configure SMTP values (`EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`,
  `EMAIL_HOST_PASSWORD`, and `DEFAULT_FROM_EMAIL`) so booking and contact workflows
  can send mail when notifications are added.
- Run `python manage.py collectstatic --noinput` and serve `STATIC_ROOT` from the
  reverse proxy. Store `MEDIA_ROOT` on persistent storage and serve it privately
  where appropriate.
- Run `python manage.py check --deploy` with production environment variables before
  release, then start the WSGI application with Gunicorn (or another production
  WSGI server), for example:
  `gunicorn config.wsgi:application --bind 0.0.0.0:8000`
- Set `SECURE_SSL_REDIRECT=True` and configure HSTS only after HTTPS is working
  end-to-end behind the reverse proxy.

Render deployment
-----------------
1. Push this project to a GitHub repository (do not commit `.env` or credentials).
2. In Render, choose **New > Blueprint**, connect the repository, and apply
   `render.yaml`. Render will create the web service and PostgreSQL database.
3. After the first deploy, open the service URL and verify `/`, `/services/`,
   `/booking/`, and `/contact/`.
4. Create the first admin account from the Render Shell with
   `python manage.py createsuperuser`.
5. Add SMTP variables in the Render service environment if email notifications
   are needed. Uploaded media is not persistent on an ordinary web service;
   use object storage or attach a persistent disk before relying on admin uploads.

Admin
-----
Create a superuser with `python manage.py createsuperuser` and then access the custom dashboard at `/admin-dashboard/login/` using the same admin credentials. The dashboard gives staff members a quick overview of customer reviews, booking enquiries, and contact messages, and lets them update review visibility and customer interaction statuses.

The default Django admin remains available at `/admin/` for full backend management.

Files of interest
-----------------
- config/settings.py - Project settings (PostgreSQL-ready)
- garage/models.py - Data models
- garage/admin.py - Admin configuration
- garage/views.py, garage/urls.py - public views
- templates/ - site templates
- static/ - CSS, JS and placeholder images

Notes
-----
Replace placeholder images in static/images and upload real media via admin for better presentation.
