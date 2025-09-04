from marshmallow import Schema, fields, validate


class PaginationMetadataSchema(Schema):
    total = fields.Int()
    total_pages = fields.Int()
    first_page = fields.Int()
    last_page = fields.Int()
    page = fields.Int()
    previous_page = fields.Int(allow_none=True)
    next_page = fields.Int(allow_none=True)


class ErrorSchema(Schema):
    code = fields.Int(description="Error code")
    status = fields.Str(description="Error name")
    message = fields.Str(description="Error message")
    errors = fields.Dict(description="Errors")


class UserRegisterSchema(Schema):
    email = fields.Email(required=True, description="User email")
    password = fields.Str(required=True, validate=validate.Length(min=6), load_only=True, description="Password")


class UserLoginSchema(Schema):
    email = fields.Email(required=True, description="User email")
    password = fields.Str(required=True, load_only=True, description="Password")


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    created_at = fields.DateTime(dump_only=True)


class TokenSchema(Schema):
    access_token = fields.Str(required=True, description="JWT access token")


class NoteCreateSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    content = fields.Str(required=True)


class NoteUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=1, max=255))
    content = fields.Str()


class NoteSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
