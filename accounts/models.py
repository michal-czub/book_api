from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)

class UserManager(BaseUserManager):
	def create_user(self, email, name, age, birthdate, password=None, is_active=True, is_staff=False, is_admin=False):
		if not email:
			raise ValueError("User must have an email!")
		if not password:
			raise ValueError("User must have a password!")
		user = self.model(
			email = self.normalize_email(email),
			name=name,
			age=age,
			birthdate=birthdate
		)
		user.set_password(password)		
		user.active = is_active
		user.staff = is_staff
		user.admin = is_admin
		user.save(using=self._db)
		return user

	def create_staffuser(self, email, name, age, birthdate, password=None):
		user = self.create_user(
			email,
			password=password,
			is_staff=True,
			name=name,
			age=age,
			birthdate=birthdate
		)
		return user

	def create_superuser(self, email, name, age, birthdate, password=None):
		user = self.create_user(
			email,
			password=password,
			is_staff=True,
			is_admin=True,
			name=name,
			age=age,
			birthdate=birthdate
		)
		return user

class User(AbstractBaseUser):
	email = models.EmailField(max_length=255, unique=True)
	name = models.CharField(max_length=100)
	age = models.IntegerField(blank=True, null=True)
	birthdate = models.DateTimeField()
	active = models.BooleanField(default=True) # can log in, and retrieve data
	staff = models.BooleanField(default=False) # employee (not super)
	admin = models.BooleanField(default=False) # super user - can add anything
	timestamp = models.DateTimeField(auto_now_add=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name', 'age', 'birthdate']

	objects = UserManager()

	def __str__(self):
		return self.email

	def get_name(self):
		return self.name

	def get_age(self):
		return self.age

	def get_birthdate(self):
		return self.birthdate

	def has_perm(self, perm, obj=None):
		return self.admin

	def has_module_perms(self, app_label):
		return self.admin

	@property
	def is_active(self):
		return self.active

	@property
	def is_staff(self):
		return self.staff

	@property
	def is_admin(self):
		return self.admin
	 
	
	
	


