from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from accounts import views

router = DefaultRouter()
router.register(r'all', views.UserViewSet)
# router.register(r'register', views.RegisterView, basename='register')

urlpatterns = [
	path("", include(router.urls)),
	path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('register/', views.RegisterView.as_view(), name='auth_register'),
	path('password/reset/', views.PasswordChangeView.as_view(), name='auth_password_reset'),
]
