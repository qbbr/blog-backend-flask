from marshmallow import validate
from flaskr import ma
from flaskr.models import User, Post, Tag


class UserRegistrationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    username = ma.auto_field(required=True, validate=[validate.Length(min=4, max=80)])
    password = ma.auto_field(required=True, validate=[validate.Length(min=6, max=255)])


class UserProfileSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = ma.auto_field(dump_only=True)
    username = ma.auto_field(dump_only=True)
    about = ma.auto_field()
    createdAt = ma.auto_field(dump_only=True)
    postsCount = ma.Function(lambda obj: len(obj.posts))


class UserPostSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field(dump_only=True)
    username = ma.auto_field(dump_only=True)


class TagSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Tag

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(validate=[validate.Length(min=2, max=32)])
    postsCount = ma.Function(lambda obj: len(obj.posts))


class PostSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Post
        load_instance = True

    id = ma.auto_field(dump_only=True)
    user = ma.Nested(UserPostSchema)
    title = ma.auto_field(required=True, validate=[validate.Length(min=2, max=255)])
    slug = ma.auto_field(dump_only=True)
    text = ma.auto_field(required=True)
    tags = ma.Nested(TagSchema, many=True)
    html = ma.auto_field(dump_only=True)
    isPrivate = ma.auto_field()
    createdAt = ma.auto_field(dump_only=True)
    updatedAt = ma.auto_field(dump_only=True)
