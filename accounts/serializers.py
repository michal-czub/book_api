from accounts.models import User
from rest_framework import serializers
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)

class UserSerializer(serializers.ModelSerializer):
	
	# books = serializers.SerializerMethodField(read_only=True)
	email = serializers.EmailField(read_only=False)
	password = serializers.CharField(style={"input_type": "password"}, write_only=True)

	# def get_books(self, instance):
	# 	return (book.get_books() for book in instance.books.all())

	class Meta:	
		model = User
		fields = (
			"id",
			"email",	
			"password",		
		)