# To-Do API

A REST API for managing to-dos, built with Flask and SQLite, with user authentication using JWT.

## Features
- User registration with bcrypt-hashed passwords
- Login with JWT tokens (expire after 2 hours)
- Each user can only see and manage their own to-dos

## Setup
```bash
pip install -r requirements.txt
```
Create a `.env` file:
```
SECRET_KEY=your-secret-key
```
Run:
```bash
python app.py
```

## Endpoints
| Method | Route | Auth | Description |
|---|---|---|---|
| POST | /register | No | Create an account |
| POST | /login | No | Get a token |
| GET | /todos | Yes | List your to-dos |
| POST | /todos | Yes | Create a to-do |
| PUT | /todos/<id> | Yes | Update a to-do |
| DELETE | /todos/<id> | Yes | Delete a to-do |

Authenticated routes need the header: `Authorization: Bearer <token>`