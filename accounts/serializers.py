from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
	
	books = serializers.SerializerMethodField(read_only=True)
	email = serializers.EmailField(read_only=False)
	# password = serializers.CharField(style={"input_type": "password"}, write_only=True)

	def get_books(self, instance):
		return (book.get_books() for book in instance.books.all())

	class Meta:	
		model = User
		fields = (
			"id",
			"url",
			"email",	
			"name",
			"age",
			"birthdate",
			# "password",
			"active",
			"staff",
			"admin",
			"timestamp",
			"books",
		)

class RegisterSerializer(serializers.ModelSerializer):

	password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
	active = serializers.BooleanField(read_only=True)

	class Meta:
		model = User
		fields = [
			"email",
			"name",
			"age",
			"birthdate",
			"password",
			"active",
			"staff",			
			"timestamp",
		]

	def create(self, validated_data):
		user = User.objects.create(
			email = validated_data['email'],
			name = validated_data['name'],
			age = validated_data['age'],
			birthdate = validated_data['birthdate'],
			staff = validated_data['staff'],
		)

		user.set_password(validated_data['password'])
		user.save()

		return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
	@classmethod
	def get_token(cls, user):
		token = super(MyTokenObtainPairSerializer, cls).get_token(user)

		token['email'] = user.email
		token['name'] = user.name
		token['age'] = user.age
		#token['birthdate'] = user.birthdate
		token['is_active'] = user.is_active
		token['is_staff'] = user.is_staff
		token['is_admin'] = user.is_admin

		return token

class PasswordChangeSerializer(serializers.ModelSerializer):
	old_password = serializers.CharField(write_only=True, required=True)
	new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
	repeat_password = serializers.CharField(write_only=True, required=True)

	class Meta:
		model = User
		fields = (
			"old_password",
			"new_password",
			"repeat_password"
		)

	def validate(self, attrs):
		if attrs["new_password"] != attrs["repeat_password"]:
			raise serializers.ValidationError({"new_password": "Password didn't match"})
		return attrs

	def validate_old_password(self, value):
		user = self.context['request'].user
		if not user.check_password(value):			
			raise serializers.ValidationError("Password is incorrect")
		return value
