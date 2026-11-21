# Ink & Insight — Full-Stack Blog Platform

A responsive editorial blogging platform built with **React, Bootstrap 5, Django, Django REST Framework, and SQLite**.

## CODTECH Internship Details

- **Intern ID:** CIS72
- **Intern Name:** Keerthana
- **Internship Duration:** 4 Weeks
- **Project Name:** Ink & Insight – Blog Platform
- **Project Type:** Python Full-Stack Web Application

## Features

- Session-based registration, login, logout, CSRF protection and profile management.
- Profile bio and avatar upload; author profile pages and published posts.
- Create, preview, save drafts, publish, edit and delete posts.
- Categories, comma-separated tags, cover images, excerpts and reading-time estimates.
- Search, category filtering, newest/oldest sorting, featured and popular sections.
- Post detail pages, likes/claps, comments, related posts and native share/copy link.
- Author dashboard with post, draft, like and comment totals.
- About, Contact and custom not-found pages.
- Seed command for categories and 10 sample posts.
- Django admin, validation, author-only permissions and database-level unique likes.
- Responsive Bootstrap layout, accessible labels, reduced-motion support and toast feedback.

## Requirements

- Python 3.10+
- Node.js 20+ and npm
- Windows, macOS or Linux

## Installation and Setup

### Windows PowerShell

Open two terminals in the extracted `blog_platform` folder.

**1. Backend setup**

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

Backend/API: http://127.0.0.1:8000

Django admin: http://127.0.0.1:8000/admin/

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**2. Frontend setup**

Open the second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal (normally http://localhost:5173).

Vite proxies `/api` and `/media` to Django.

You can also launch the backend or frontend from the project root with `run_backend.ps1` and `run_frontend.ps1` in separate PowerShell windows.

### macOS / Linux Setup

**Backend:**

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

**Frontend (in another terminal):**

```bash
cd frontend
npm install
npm run dev
```

## Demo Content and Accounts

`python manage.py seed_demo` creates editorial categories and 10 sample posts authored by a demo user (`demo_author`).

It does not create a password or publish any real credentials. Create a password for that user in Django admin, or register your own account and create posts.

To access the admin, create a superuser with `createsuperuser`.

## Running Checks

**Backend tests:**

```bash
cd backend
python manage.py test blogs
```

**Frontend production build:**

```bash
cd frontend
npm install
npm run build
```

## API Overview

- `GET /api/csrf/`
- `POST /api/auth/register/`, `POST /api/auth/login/`, `POST /api/auth/logout/`
- `GET/PATCH /api/auth/me/`
- `GET/POST /api/posts/`, `GET/PATCH/DELETE /api/posts/<slug>/`
- `POST /api/posts/<slug>/like/`
- `GET/POST /api/posts/<slug>/comments/`
- `PATCH/DELETE /api/comments/<id>/`
- `GET /api/categories/`, `GET /api/dashboard/`, `GET /api/profiles/<username>/`

## Notes and Limitations

- This repository is a locally runnable development project, not a hosted production deployment. Before public deployment, configure HTTPS, secure cookies, allowed hosts, a production web server, static/media storage, backups, email verification/password reset and a production-grade database.
- Profile and cover uploads are stored locally in `backend/media/`. Image upload validation checks file type and size; production should also re-encode images and scan uploads.
- The contact page is a front-end contact form with local validation; no email delivery service is configured.
- Rich text formatting uses a constrained editor toolbar that inserts semantic HTML. Server output is sanitized before rendering.
- React development server and Django API are separate processes. No paid service is required.

## Build Verification Note

The source files, Python syntax, React/JSX syntax, package manifest, and ZIP archive were checked during preparation. Full Django runtime/API tests and the Vite production build could not be executed in the preparation environment because outbound package downloads were unavailable.

Run the installation and check commands above on your computer after dependencies are installed. The included Django test suite covers public-feed visibility, like toggling/uniqueness behavior, and author-only editing.
