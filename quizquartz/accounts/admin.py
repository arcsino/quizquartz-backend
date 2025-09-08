from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff", "is_active", "id")
    search_fields = ("username",)
    readonly_fields = ("id",)
    ordering = ("username",)
