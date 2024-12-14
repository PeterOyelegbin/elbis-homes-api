from django.contrib import admin
from .models import UserModel

# Register your models here.
@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "is_staff", "date_joined")
    list_filter = ("is_staff",)
    