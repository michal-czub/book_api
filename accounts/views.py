from django.shortcuts import render

from rest_framework import views, viewsets, generics, mixins, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.models import User
from accounts.serializers import UserSerializer, RegisterSerializer, MyTokenObtainPairSerializer
from accounts.serializers import PasswordChangeSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = User.objects.all()
	permission_classes = [IsAdminUser]
	serializer_class = UserSerializer

class RegisterView(generics.CreateAPIView):
#class RegisterView(viewsets.GenericViewSet, mixins.CreateModelMixin):
	queryset = User.objects.all()
	permission_classes = [AllowAny]
	serializer_class = RegisterSerializer

	# def perform_create(self, serializer):
	# 	if not self.request.user.admin:
	# 		raise SuperuserException()
	# 	serializer.save()

class MyTokenObtainPairView(TokenObtainPairView):
	permission_classes = [AllowAny,]
	serializer_class = MyTokenObtainPairSerializer

class PasswordChangeView(generics.UpdateAPIView):
	queryset = User.objects.all()
	serializer_class = PasswordChangeSerializer

	def get_object(self, queryset=None):
		obj = self.request.user
		return obj

	def update(self, request, *args, **kwargs):
		self.object = self.get_object()
		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():
			self.object.set_password(serializer.data.get("new_password"))
			self.object.save()
			return Response({"detail": "Password has been changed"}, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)		
