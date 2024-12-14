from django.contrib import admin
from .models import Property

# Register your models here.
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "property_type", "price", "status", "created_on")
    list_filter = ("property_type", "status")
