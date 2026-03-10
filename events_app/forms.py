from django import forms

from .models import Category, Event


class EventSubmissionForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "location",
            "start_datetime",
            "end_datetime",
            "category",
            "contact_name",
            "contact_email",
        ]
        widgets = {
            "start_datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.order_by("name")
        for field_name, field in self.fields.items():
            if field_name in {"description"}:
                field.widget.attrs.update({"rows": 5})
            field.widget.attrs.setdefault("class", "form-control")

    def clean(self):
        cleaned_data = super().clean()
        start_datetime = cleaned_data.get("start_datetime")
        end_datetime = cleaned_data.get("end_datetime")
        if start_datetime and end_datetime and end_datetime <= start_datetime:
            self.add_error(
                "end_datetime",
                "End date and time must be later than the start date and time.",
            )
        return cleaned_data
