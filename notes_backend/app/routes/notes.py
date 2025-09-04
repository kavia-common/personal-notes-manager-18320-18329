from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint

from ..auth import require_auth
from ..repository import NoteRepository, UserRepository
from ..schemas import NoteCreateSchema, NoteSchema, NoteUpdateSchema

blp = Blueprint("Notes", "notes", url_prefix="/notes", description="Notes management endpoints")


@blp.route("")
class NotesListCreate(MethodView):
    """List and create notes."""

    @blp.response(
        200,
        NoteSchema(many=True),
        examples={"application/json": [{"id": 1, "title": "Sample", "content": "Hello", "user_id": 1}]},
    )
    @blp.doc(
        summary="List notes",
        description="Return a paginated list of notes for the current user. Pagination via ?page=&page_size=",
        responses={200: {"description": "List of notes"}},
    )
    def get(self):
        """List notes for current user with pagination."""
        email = require_auth()
        user = UserRepository.get_by_email(email)
        page = int(request.args.get("page", "1"))
        page_size = int(request.args.get("page_size", "20"))
        items, meta = NoteRepository.list_notes(user, page=page, page_size=page_size)
        # Include metadata in response headers for simplicity
        from flask import jsonify
        response = jsonify([NoteSchema().dump(n) for n in items])
        response.headers["X-Pagination-Total"] = meta["total"]
        response.headers["X-Pagination-Total-Pages"] = meta["total_pages"]
        response.headers["X-Pagination-Page"] = meta["page"]
        response.headers["X-Pagination-Next"] = meta["next_page"]
        response.headers["X-Pagination-Prev"] = meta["previous_page"]
        return response

    @blp.arguments(NoteCreateSchema, location="json")
    @blp.response(201, NoteSchema)
    @blp.doc(summary="Create note", description="Create a new note for the current user.")
    def post(self, data):
        """Create a note for the current user."""
        email = require_auth()
        user = UserRepository.get_by_email(email)
        note = NoteRepository.create_note(user, title=data["title"], content=data["content"])
        return note


@blp.route("/<int:note_id>")
class NoteDetail(MethodView):
    """Retrieve, update, and delete a note."""

    @blp.response(200, NoteSchema)
    @blp.doc(summary="Get note", description="Retrieve a single note by id.")
    def get(self, note_id: int):
        """Get a specific note."""
        email = require_auth()
        user = UserRepository.get_by_email(email)
        note = NoteRepository.get_note(user, note_id)
        return note

    @blp.arguments(NoteUpdateSchema, location="json")
    @blp.response(200, NoteSchema)
    @blp.doc(summary="Update note", description="Update title and/or content of a note.")
    def patch(self, data, note_id: int):
        """Partial update of a note."""
        email = require_auth()
        user = UserRepository.get_by_email(email)
        note = NoteRepository.update_note(user, note_id, title=data.get("title"), content=data.get("content"))
        return note

    @blp.response(204)
    @blp.doc(summary="Delete note", description="Delete a note by id.")
    def delete(self, note_id: int):
        """Delete a note."""
        email = require_auth()
        user = UserRepository.get_by_email(email)
        NoteRepository.delete_note(user, note_id)
        return "", 204
