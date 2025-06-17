from django.contrib.auth.models import User
from django.db.models import (ForeignKey, DO_NOTHING, CASCADE, CharField, DateTimeField, Model, TextField, ImageField,
                              EmailField, FileField, OneToOneField)
from django.db.models.fields import BooleanField


class BusinessType(Model):
    name = CharField(max_length=128)

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return f'{self.name}'


class Region(Model):
    name = CharField(max_length=128)

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return f'{self.name}'


class District(Model):
    name = CharField(max_length=128)
    region_id = ForeignKey(Region, on_delete=DO_NOTHING)

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return f'{self.name}'


class Position(Model):
    name = CharField(max_length=128)

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return f'{self.name}'


class Client(Model):
    user = OneToOneField(User, null=True, on_delete=DO_NOTHING)
    business_type = ForeignKey(BusinessType, on_delete=DO_NOTHING)
    address = CharField(max_length=128)
    city = CharField(max_length=20)
    district = ForeignKey(District, on_delete=DO_NOTHING)
    business_name = CharField(max_length=30)
    VAT_number = CharField(max_length=50)
    logo = ImageField(null=True, blank=True)
    contact_email = EmailField(null=True)
    contact_phone = CharField(max_length=15)

    def __repr__(self):
        return f'{self.business_name} ({self.address})'

    def __str__(self):
        return f'{self.business_name} ({self.address})'


class Advertisement(Model):
    position = ForeignKey(Position, on_delete=DO_NOTHING)
    title = CharField(max_length=128)
    text_content = TextField()
    salary = CharField(max_length=128)
    client = ForeignKey(Client, on_delete=DO_NOTHING, null=True, related_name="advertisements")
    created = DateTimeField(auto_now_add=True)
    created_by = ForeignKey(User, on_delete=CASCADE, null=True)
    highlight = BooleanField(default=False)
    published = BooleanField(default=False)

    class Meta:
        permissions = [('can_create_ad', 'Can create advertisement')]
        ordering = ['-highlight', '-created']

    def __repr__(self):
        return f'{self.title}'

    def __str__(self):
        return f'{self.title}'


class Response(Model):
    advertisement = ForeignKey(Advertisement, on_delete=DO_NOTHING, related_name='responses')
    name = CharField(max_length=100)
    email = EmailField()
    message = TextField()
    created = DateTimeField(auto_now_add=True)
    cv = FileField(upload_to='cvs/', null=True, blank=True)

    def __repr__(self):
        return f'{self.advertisement}'

    def __str__(self):
        return f'{self.advertisement}'


class Contacts(Model):
    class Meta:
        verbose_name_plural = "Contacts"
    name = CharField(max_length=128)
    role = CharField(max_length=128)
    email = EmailField()
    phone = CharField(max_length=15)

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return f'{self.name}'


