from django.core.exceptions import ValidationError
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="events"
    )
    contact_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["start_datetime", "title"]

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if (
            self.end_datetime
            and self.start_datetime
            and self.end_datetime <= self.start_datetime
        ):
            raise ValidationError(
                {
                    "end_datetime": "End date and time must be later than the start date and time."
                }
            )
