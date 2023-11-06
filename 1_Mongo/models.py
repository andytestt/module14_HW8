from mongoengine import Document, CASCADE
from mongoengine.fields import ReferenceField, ListField, StringField
import connect



class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Qoute(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    qoute = StringField()
    meta = {'allow_inheritance': True}