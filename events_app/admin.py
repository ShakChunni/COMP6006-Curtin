from django.contrib import admin
from django.utils import timezone

from .models import Category, Event


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "start_datetime", "is_approved", "approved_at")
    list_filter = ("is_approved", "category")
    search_fields = (
        "title",
        "description",
        "location",
        "contact_name",
        "contact_email",
    )
    readonly_fields = ("created_at",)

    def save_model(self, request, obj, form, change):
        # Keep the approval timestamp in step with moderation changes.
        if obj.is_approved and obj.approved_at is None:
            obj.approved_at = timezone.now()
        if not obj.is_approved:
            obj.approved_at = None
        super().save_model(request, obj, form, change)
