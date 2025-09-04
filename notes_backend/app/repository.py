from typing import List, Optional, Tuple

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound, Conflict

from .models import db, User, Note


class UserRepository:
    """Data access for User."""

    @staticmethod
    def create_user(email: str, password: str) -> User:
        existing = User.query.filter_by(email=email).first()
        if existing:
            raise Conflict("Email already registered")
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError as exc:
            db.session.rollback()
            raise Conflict("Email already registered") from exc
        return user

    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        return User.query.filter_by(email=email).first()


class NoteRepository:
    """Data access for Note with user scoping."""

    @staticmethod
    def create_note(user: User, title: str, content: str) -> Note:
        note = Note(user_id=user.id, title=title, content=content)
        db.session.add(note)
        db.session.commit()
        return note

    @staticmethod
    def list_notes(user: User, page: int = 1, page_size: int = 20) -> Tuple[List[Note], dict]:
        q = Note.query.filter_by(user_id=user.id).order_by(Note.created_at.desc())
        pagination = q.paginate(page=page, per_page=page_size, error_out=False)
        meta = {
            "total": pagination.total,
            "total_pages": pagination.pages or 1,
            "first_page": 1,
            "last_page": pagination.pages or 1,
            "page": pagination.page,
            "previous_page": pagination.prev_num if pagination.has_prev else None,
            "next_page": pagination.next_num if pagination.has_next else None,
        }
        return list(pagination.items), meta

    @staticmethod
    def get_note(user: User, note_id: int) -> Note:
        note = Note.query.filter_by(id=note_id, user_id=user.id).first()
        if not note:
            raise NotFound("Note not found")
        return note

    @staticmethod
    def update_note(user: User, note_id: int, title: Optional[str] = None, content: Optional[str] = None) -> Note:
        note = NoteRepository.get_note(user, note_id)
        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        db.session.commit()
        return note

    @staticmethod
    def delete_note(user: User, note_id: int) -> None:
        note = NoteRepository.get_note(user, note_id)
        db.session.delete(note)
        db.session.commit()
