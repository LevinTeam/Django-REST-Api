from django.contrib import admin
from .models import CommentsData, Users
# Register your models here.

class CommentsAdminView(admin.ModelAdmin):
    list_comments = ('name', 'email', 'phone', 'subject', 'message')
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message']

admin.site.register(CommentsData, CommentsAdminView)


class UsersAdminView(admin.ModelAdmin):
    list_comments = ('firstname', 'lastname', 'email', 'phone', 'password')
    # readonly_fields = ['firstname', 'lastname', 'email', 'phone', 'password']

admin.site.register(Users, UsersAdminView)