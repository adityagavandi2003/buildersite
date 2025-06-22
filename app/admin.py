from django.contrib import admin
from app.models import AbstractUser,Cutomer

# Register your models here.

@admin.register(AbstractUser)
class AbtractUserAdmin(admin.ModelAdmin):
    list_display = ['user','category','created_at']

@admin.register(Cutomer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name','location','phone_number','email','budget','property_type','agent']
    search_fields = ['name','location','budget','property_type']