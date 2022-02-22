from django.db.models import Avg, Count, Max, Min
from django.utils import timezone

from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator, UniqueForYearValidator

from book.models import Book, PublishingHouse, Author, Library

class NameValidator:
	def __call__(self, value):
		if value[0].islower(): raise serializers.ValidationError("Must begin with an uppercase letter.")

class PublishingHouseSerializer(serializers.ModelSerializer):
	name = serializers.CharField(validators=[NameValidator()])
	year_of_foundation = serializers.HiddenField(default=timezone.now)
	books = serializers.SerializerMethodField(read_only=True)

	validators = [
		UniqueForYearValidator(
			queryset=PublishingHouse.objects.all(),
			field="name",
			date_field="year_of_foundation",
			message="Name must be unique for the given year {}".format(timezone.now())			
		)
	]

	# def validate_name(self, value):
	# 	if value[0].islower():
	# 		raise serializers.ValidationError("Name must begin with an uppercase letter!")		

	def get_books(self, instance):
		return (book.get_books() for book in instance.books.all())	

	class Meta:
		model = PublishingHouse
		fields = (
			"id",
			"url",
			"name",
			"year_of_foundation",
			"books",
		)

class BookSerializer(serializers.ModelSerializer):
	# author = serializers.ReadOnlyField(source=author.name)
	# include infos about publishing house
	# publishing_house = serializers.ReadOnlyField(source='publishing_house.name')
	#publishing_house_name = serializers.ReadOnlyField(source='publishinghouse.name')
	#authors = AuthorSerializer(many=True, read_only=True)
	# ph = PublishingHouseSerializer(many=True, read_only=True)	
	# def get_publishing_details(self, instance):
	# 	return (ph.get_details() for ph in instance.books.all())

	#authors_general = serializers.SerializerMethodField()
	#author = serializers.SerializerMethodField(read_only=True)
	# #def get_authors_general(self, instance):
	# 	return (author.get_author_details() for author in instance.authors_general.all())
	title = serializers.CharField(validators=[NameValidator()])
	publishing_house = serializers.SerializerMethodField()
	library_details = serializers.SerializerMethodField(read_only=True)	
	library_name = serializers.SerializerMethodField(read_only=True)
	created_by = serializers.CharField(read_only=True)
	updated_by = serializers.CharField(read_only=True, required=False)
	avg_rating = serializers.SerializerMethodField()
	user = serializers.SerializerMethodField()
	author = serializers.SerializerMethodField()

	validators = [
		UniqueTogetherValidator(
			queryset=Book.objects.all(),
			fields=['title', 'description']
		)
	]

	def validate_rating(self, value):
		if value <= 0 or value >= 10: raise serializers.ValidationError("Pass rating between 0 and 10")

	# def validate_title(self, value):
	# 	if value[0].islower():
	# 		raise serializers.ValidationError("Title must begin with an uppercase letter!")

	def get_author(self, instance):
		return (author.get_author_details() for author in instance.author.all())
		# for author in instance.author.all():
			#return author.get_author_details()			

	def get_publishing_house(self, instance):
		return instance.get_publish()

	def get_library_details(self, instance):
		return instance.get_library_details()

	def get_library_name(self, instance):
		return instance.get_library_name()

	def get_user(self, instance):
		return instance.get_user_details()

	def get_avg_rating(self, instance):
		return (Book.objects.aggregate(Avg('rating')))

	class Meta:
		model = Book
		fields = (
			"id",
			"url",
			"title",
			"description",
			"pages",
			"rating",
			"is_borrowed",
			"category",
			"release_date",
			"created_by",
			"updated_by",
			"publishinghouse",			
			"publishing_house",
			"author",	
			"library",
			"library_details",
			"library_name",
			"avg_rating",
			"user",		
		)

class AuthorSerializer(serializers.ModelSerializer):
	name = serializers.CharField(validators=[NameValidator(),
		UniqueValidator(queryset=Author.objects.all())])
	books_general = serializers.SerializerMethodField(read_only=True)
	books = BookSerializer(many=True, read_only=True)
	lowest_highest_rating = serializers.SerializerMethodField()

	def validate_age(self, value):
		if value <= 0: raise serializers.ValidationError("Age must be at least 1")

	def get_books_general(self, instance):
		return (book.get_books() for book in instance.books.all())

	def get_lowest_highest_rating(self, instance):
		return Author.objects.aggregate(min_rating=Min('books__rating'), max_rating=Max('books__rating'))

	class Meta:
		model = Author
		fields = (
			"id",
			"url",
			"name",
			"age",
			"country",
			"books",
			"books_general",
			"lowest_highest_rating",
		)	

class LibrarySerializer(serializers.ModelSerializer):
	name = serializers.CharField(validators=[NameValidator(),
		UniqueValidator(queryset=Library.objects.all())])
	books = serializers.SerializerMethodField()
	aggregated_rating = serializers.SerializerMethodField()
	#total_book_count = serializers.SerializerMethodField()

	def get_books(self, instance):
		return (book.get_books() for book in instance.books.all())

	## Aggregate
	def get_aggregated_rating(self, instance):
		return (Book.objects.aggregate(average_rating=Avg('rating'), max_rating=Max('rating'), min_rating=Min('rating')))




	class Meta:
		model = Library
		fields = (
			"id",
			"url",
			"name",
			"address",			
			"books",
			#"total_book_count",
			"aggregated_rating",
		)
