from mongoengine import Document
from mongoengine.fields import StringField, BooleanField, IntField


class Contact(Document):
    completed = BooleanField(default=False)
    fullname = StringField(max_length=250, required=True)
    address = StringField(max_length=250)
    job = StringField(max_length=250)
    company = StringField(max_length=250)
    phone_number = StringField(max_length=250)
    email = StringField(max_length=250)
    num = IntField()
    meta = {"collection": 'contacts'}

