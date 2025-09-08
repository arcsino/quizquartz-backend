from django.contrib import admin
from .models import Tag, QuizGroup, Quiz


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "is_private", "id")
    search_fields = ("name",)
    readonly_fields = ("id",)
    ordering = ("name",)


@admin.register(QuizGroup)
class QuizGroupAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "created_at", "updated_at", "id")
    search_fields = ("title", "created_by__username")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("question", "related_group", "created_by", "id")
    search_fields = ("question", "created_by__username", "related_group__title", "id")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)
