from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# SQLAlchemy instance (initialized in app factory)
db = SQLAlchemy()


class User(db.Model):
    """User model representing application users authenticated via email/password."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    notes = db.relationship("Note", backref="user", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        """Hash and set password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify provided password against stored hash."""
        return check_password_hash(self.password_hash, password)


class Note(db.Model):
    """Note model representing personal notes created by users."""
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
