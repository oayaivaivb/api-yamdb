"""Модуль административной панели для приложения reviews."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Category, Genre, Title, Review, Comment


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Дополнительные поля', {'fields': ('bio', 'role', 'confirmation_code')}),
    )
    list_display = BaseUserAdmin.list_display + ('role',)
    list_filter = BaseUserAdmin.list_filter + ('role',)
    search_fields = ('username', 'email')
    readonly_fields = ('confirmation_code',)

    @admin.display(description='Количество отзывов')
    def reviews_count(self, obj):
        return obj.reviews.count()

    @admin.display(description='Количество комментариев')
    def comments_count(self, obj):
        return obj.comments.count()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'category')
    search_fields = ('name',)
    list_filter = ('category',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'score', 'pub_date')
    search_fields = ('text',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'author', 'pub_date')
    search_fields = ('text',)
