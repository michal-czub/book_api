from django.contrib import admin

# Register your models here.
from .models import Book, Author, PublishingHouse, Library

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(PublishingHouse)
admin.site.register(Library)