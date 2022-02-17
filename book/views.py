from book.models import Book, PublishingHouse, Author, Library
from book.serializers import BookSerializer, PublishingHouseSerializer, AuthorSerializer
from book.serializers import LibrarySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from django.http import Http404
from rest_framework import generics, mixins

from django.db.models import Q, Avg
from django.db.models.functions import Concat

# class BookList(APIView):
# 	def get(self, request):
# 		data = Book.objects.all()
# 		serializer = BookSerializer(data, many=True)
# 		return Response(serializer.data)

# 	def post(self, request):
# 		serializer = BookSerializer(data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data, status=status.HTTP_201_CREATED)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookViewSet(viewsets.ModelViewSet):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

	def perform_create(self, serializer):
		serializer.save(created_by=self.request.user.name, user=self.request.user)

	def perform_update(self, serializer):
		serializer.save(updated_by=self.request.user.name)

class BorrowedBooksViewSet(viewsets.ReadOnlyModelViewSet):	
	queryset = Book.objects.filter(is_borrowed=True, )
	serializer_class = BookSerializer

class Test(viewsets.ReadOnlyModelViewSet):
	queryset = Book.objects.all()
	serializer_class = BookSerializer

	def get_queryset(self):
		return super().get_queryset().filter(pages=333)

# class Test2(APIView):
# 	def get(self, request, **kwargs):
# 		query = request.query_params.get("phrase")
# 		queryset = Book.objects.filter(description=query)
# 		serializer = BookSerializer(queryset)
# 		return Response(serializer.data)

# class SearchBookAPIView(APIView):
# 	def get(self, request, *args, **kwargs):
# 		query = request.query_params.get("phrase")
# 		search_name = Q(search_name__icontains=query)
# 		books = Book.objects.annotate(
# 			search_name=Concat('first_')
# 			)

class PublishingHouseViewSet(viewsets.ModelViewSet):
	queryset = PublishingHouse.objects.all()
	serializer_class = PublishingHouseSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# class AuthorList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
# 	queryset = Author.objects.all()
# 	serializer_class = AuthorSerializer

# 	def get(self, request, *args, **kwargs):
# 		return self.list(request, *args, **kwargs)

# 	def post(self, request, *args, **kwargs):
# 		return self.create(request, *args, **kwargs)

# class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
# 	queryset = Author.objects.all()
# 	serializer_class = AuthorSerializer

class AuthorViewSet(viewsets.ModelViewSet):
	queryset = Author.objects.all()
	serializer_class = AuthorSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class LibraryViewSet(viewsets.ModelViewSet):
	queryset = Library.objects.all()
	serializer_class = LibrarySerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]