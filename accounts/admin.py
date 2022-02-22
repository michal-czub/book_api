from django.contrib import admin
# from django.contrib.auth import get_user_model
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

class UserAdmin(admin.ModelAdmin):
	search_fields = ['email']
	list_display = ('name', 'email', 'pk',)
	list_filter = ('name', 'email')
	class Meta:
		model = User

# class UserAdmin(BaseUserAdmin):
#     # The forms to add and change user instances
#     form = UserAdminChangeForm
#     add_form = UserAdminCreationForm

#     # The fields to be used in displaying the User model.
#     # These override the definitions on the base UserAdmin
#     # that reference specific fields on auth.User.
#     list_display = ['email', 'admin']
#     list_filter = ['admin']
#     fieldsets = (
#         (None, {'fields': ('email', 'password', 'name', 'age', 'birthdate')}),
#         ('Personal info', {'fields': ()}),
#         ('Permissions', {'fields': ('admin', 'active', 'staff')}),
#     )
#     # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
#     # overrides get_fieldsets to use this attribute when creating a user.
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password')}
#         ),
#     )
#     search_fields = ['email']
#     ordering = ['email']
#     filter_horizontal = ()
admin.site.site_header = "Bookshop Admin Panel"

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
# admin.site.unregister(Groups)
# admin.site.register(User)
