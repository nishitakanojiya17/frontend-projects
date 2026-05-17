# Campus Mitra — Backend Setup Guide

## Prerequisites
- Python 3.10+
- MySQL 8.0 running locally
- The `.venv` already exists in the parent folder (or create a new one)

---

## Step 1 — Create the MySQL database

Open MySQL Workbench or the MySQL shell and run:

```sql
CREATE DATABASE campus_mitra_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

If you want a dedicated user instead of root:
```sql
CREATE USER 'campusmitra'@'localhost' IDENTIFIED BY 'yourpassword';
GRANT ALL PRIVILEGES ON campus_mitra_db.* TO 'campusmitra'@'localhost';
FLUSH PRIVILEGES;
```
Then update `DB_USER` and `DB_PASSWORD` in `.env`.

---

## Step 2 — Install dependencies

From the `backend/` folder:

```bash
# Activate the venv (Windows)
..\.venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

---

## Step 3 — Configure .env

Edit `backend/.env` and set your MySQL root password:

```
DB_PASSWORD=your_mysql_root_password
```

---

## Step 4 — Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Step 5 — Seed all users

This creates all departments, students (AIML/CS/IT/ME), faculty, and demo accounts:

```bash
python manage.py seed_users
```

---

## Step 6 — Start the server

```bash
python manage.py runserver
```

API is live at: **http://127.0.0.1:8000/api/**

---

## Test the login API

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"nishita.kanojiya@iist.ac.in\", \"password\": \"nishita@123\"}"
```

Expected response:
```json
{
  "access": "<jwt_token>",
  "refresh": "<refresh_token>",
  "role": "student",
  "name": "Nishita Kanojiya",
  "email": "nishita.kanojiya@iist.ac.in",
  "enrollment_no": "2022AIML001",
  "semester": 6,
  "section": "A",
  "department": "Artificial Intelligence & Machine Learning",
  "branch_code": "AIML"
}
```

---

## Quick Credentials Reference

| Role    | Email                      | Password     |
|---------|----------------------------|--------------|
| Student | student@iist.ac.in         | student123   |
| Faculty | faculty@iist.ac.in         | faculty123   |
| Parent  | parent@iist.ac.in          | parent123    |
| Admin   | admin@iist.ac.in           | admin123     |
| Student | nishita.kanojiya@iist.ac.in | nishita@123 |
| Faculty | ratnesh.chaturvedi@iist.ac.in | ratnesh@123 |

Full list in `../CREDENTIALS.md`.

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/auth/login/` | None | Login → JWT + role |
| POST | `/api/auth/refresh/` | None | Refresh access token |
| GET | `/api/auth/me/` | Any | Current user profile |
| GET | `/api/attendance/my/` | Student | Subject-wise attendance |
| POST | `/api/attendance/mark/` | Faculty | Mark attendance |
| GET | `/api/notes/` | Student | List notes |
| POST | `/api/notes/upload/` | Faculty | Upload note |
| GET | `/api/announcements/` | Any | Role-filtered announcements |
| POST | `/api/announcements/new/` | Faculty/Admin | Post announcement |
| GET | `/api/timetable/` | Student/Faculty | View timetable |
| GET | `/api/subjects/` | Any | List subjects |
| GET | `/api/departments/` | None | List departments |
| GET | `/api/parent/children/` | Parent | Child profile |
| GET | `/api/admin/users/` | Admin | All users |
| GET | `/api/admin/alerts/` | Admin | Low attendance alerts |
| GET | `/api/admin/students/?dept=AIML` | Admin | Students by dept |
| GET | `/api/admin/faculty/?dept=CS` | Admin | Faculty by dept |
