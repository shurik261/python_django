from django.contrib import admin

from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = [ProfileInline, ]
    fieldsets = [
        (None, {'fields': ('avatar',)}),
    ]




