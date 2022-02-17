from rest_framework import serializers
from book.models import Book, PublishingHouse, Author, Library
from django.db.models import Avg, Count, Max, Min

class PublishingHouseSerializer(serializers.ModelSerializer):
	books = serializers.SerializerMethodField(read_only=True)


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
	publishing_house = serializers.SerializerMethodField()
	library_details = serializers.SerializerMethodField(read_only=True)	
	library_name = serializers.SerializerMethodField(read_only=True)
	created_by = serializers.CharField(read_only=True)
	updated_by = serializers.CharField(read_only=True, required=False)
	avg_rating = serializers.SerializerMethodField()

	def get_publishing_house(self, instance):
		return instance.get_publish()

	def get_library_details(self, instance):
		return instance.get_library_details()

	def get_library_name(self, instance):
		return instance.get_library_name()

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
		)

class AuthorSerializer(serializers.ModelSerializer):
	books_general = serializers.SerializerMethodField(read_only=True)
	books = BookSerializer(many=True, read_only=True)
	lowest_highest_rating = serializers.SerializerMethodField()

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
