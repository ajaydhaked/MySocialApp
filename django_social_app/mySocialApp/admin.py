from django.contrib import admin

from django.contrib.auth.models import Group,User
from django.contrib.auth import models

from .models import Profile , Dweet
class ProfileInline(admin.StackedInline):
    model = Profile
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username','email','password']
    inlines= [ProfileInline]
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Dweet)
# admin.site.register(Profile)

