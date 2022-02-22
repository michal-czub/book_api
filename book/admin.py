from django.contrib import admin
from .models import Book, Author, PublishingHouse, Library

class AuthorAdmin(admin.ModelAdmin):
	search_fields = ['name']
	list_filter = ['name', 'country',]
	list_display = ['name', 'age', 'pk']

class PublishingHouseAdmin(admin.ModelAdmin):
	search_fields = ['name']
	list_filter = ['name']
	list_display = ['name', 'year_of_foundation', 'pk']

class LibraryAdmin(admin.ModelAdmin):
	search_fields = ['name']
	list_filter = ['name', 'address']
	list_display = ['name', 'address', 'pk']

class BookAdmin(admin.ModelAdmin):
	search_fields = ['title']
	list_filter = ['category', 'author', 'library', 'publishinghouse']
	list_display = ['title', 'pages', 'is_borrowed', 'pk']

admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(PublishingHouse, PublishingHouseAdmin)
admin.site.register(Library, LibraryAdmin)
