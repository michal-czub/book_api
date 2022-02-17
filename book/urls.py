from django.urls import path, include
from book import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books', views.BookViewSet)
#router.register(r'borrowed-books', views.BorrowedBooksViewSet)
# router.register(r'test', views.Test)
router.register(r'publish', views.PublishingHouseViewSet)
router.register(r'authors', views.AuthorViewSet)
router.register(r'libraries', views.LibraryViewSet)

urlpatterns = [
	path('', include(router.urls)),
	#path("search", views.Test2.as_view())	
	# path('authors/', views.AuthorList.as_view()),
	# path('authors/<int:pk>/', views.AuthorDetail.as_view()),
]