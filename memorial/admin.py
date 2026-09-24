from django.contrib import admin

from .models import LifeChapter, MemorialQuote, Tribute


@admin.register(LifeChapter)
class LifeChapterAdmin(admin.ModelAdmin):
    list_display = ("year", "title", "order")
    list_editable = ("order",)


@admin.register(Tribute)
class TributeAdmin(admin.ModelAdmin):
    list_display = ("author_name", "relationship", "is_approved", "created_at")
    list_filter = ("is_approved",)
    search_fields = ("author_name", "message")


@admin.register(MemorialQuote)
class MemorialQuoteAdmin(admin.ModelAdmin):
    list_display = ("text", "attribution", "is_active")
    list_filter = ("is_active",)
