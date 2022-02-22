from django.db import models
from accounts.models import User


class PublishingHouse(models.Model):
	name = models.CharField(max_length=200)
	year_of_foundation = models.DateTimeField(auto_now_add=True)	

	def get_publish_details(self):
		return {
			"id": self.id,			
			"name": self.name,
			"year_of_foundation": self.year_of_foundation
		}

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']

class Author(models.Model):

	POLAND = "Poland"
	GERMANY = "Germany"
	UK = "UK"

	COUNTRY_CHOICE = [
		(POLAND, 'Poland'),
		(GERMANY, 'Germany'),
		(UK, 'UK'),
	]

	name = models.CharField(max_length=100)
	age = models.IntegerField()
	country = models.CharField(choices=COUNTRY_CHOICE, max_length=10)
#	authors_general = self.get_author_details()

	def get_author_details(self):
		return {
			"id": self.id,
			"name": self.name,
			"age": self.age,
			"country": self.country
		}

	def __str__(self):
		return self.name

class BookManager(models.Manager):
	def smaller_than(self, size):
		return self.filter(pages__lt=size)

	def greater_than(self,size):
		return self.filter(pages__gt=size)

class Book(models.Model):
	DRAMA = 'Drama'
	POEM = 'Poem'
	ADVENTURE = 'Adventure'
	CRIMINAL = 'Criminal'
	BIOGRAPHY = 'Biography'

	CATEGORY_CHOICES = [
		(DRAMA, 'Drama'),
		(POEM, 'Poem'),
		(ADVENTURE, 'Adventure'),
		(CRIMINAL, 'Criminal'),
		(BIOGRAPHY, 'Biography'),
	]

	category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
	title = models.CharField(max_length=200, blank=True, default='')
	pages = models.IntegerField()
	description = models.CharField(max_length=300, default='', blank=True)
	release_date = models.DateTimeField(auto_now_add=True)
	is_borrowed = models.BooleanField(default=False)
	created_by = models.CharField(max_length=100, blank=True, default='')
	updated_by = models.CharField(max_length=100, blank=True, default='')
	rating = models.FloatField(default=5.0)

	author = models.ManyToManyField(Author, related_name='books')
	user = models.ForeignKey('accounts.User', related_name='books', on_delete=models.CASCADE)
	library = models.ForeignKey('Library', related_name='books', on_delete=models.CASCADE)
	publishinghouse = models.ForeignKey(PublishingHouse, related_name='books', on_delete=models.CASCADE)

	objects = BookManager()

	def get_publish(self):
		return self.publishinghouse.get_publish_details()

	def get_library_details(self):
		return self.library.get_details()

	def get_library_name(self):
		return self.library.get_library_name()

	def get_user_details(self):
		return self.user.get_details()
		
	def get_books(self):
		return {			
			"status": self.is_borrowed_info(),
			"title": self.title,
			"pages": self.pages,
			"release_date": self.release_date,
			"rating": self.rating	
		}

	def is_borrowed_info(self):
		return "This book has been borrowed" if self.is_borrowed else "This book is free to borrow"

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['id']

class Library(models.Model):
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=50)
	# book = models.ForeignKey('Book', related_name='library', on_delete=models.CASCADE)

	# books-list
	# USER - employee
	#def get_books(self):
	#	return self.book.get_books()

	def get_details(self):
		return {
			"id": self.id,
			"name": self.name,
			"address": self.address,			
		}

	def get_library_name(self):
		return {
			"name": self.name
		}

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']
