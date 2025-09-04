# Notes Backend

Flask backend for a personal notes manager. Provides authentication and CRUD for notes with OpenAPI docs.

## Quick start

1. Create and activate a virtualenv (optional).

2. Install dependencies:
   pip install -r requirements.txt

3. Configure environment:
   - Copy .env.example to .env and adjust as needed.
   - Defaults to a local SQLite file `notes.db` in the project folder.

4. Run:
   python run.py

Docs will be available at /docs (OpenAPI/Swagger UI).

## API overview

- Health: GET /
- Auth:
  - POST /auth/register {email, password}
  - POST /auth/login {email, password} -> {access_token}
  - GET  /auth/me (Authorization: Bearer <token>)
- Notes:
  - GET    /notes (Authorization required) ?page=&page_size=
  - POST   /notes {title, content} (Authorization required)
  - GET    /notes/<id> (Authorization required)
  - PATCH  /notes/<id> {title?, content?} (Authorization required)
  - DELETE /notes/<id> (Authorization required)

Authorization header:
  Authorization: Bearer <access_token>
