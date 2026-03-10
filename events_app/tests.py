from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import EventSubmissionForm
from .models import Category, Event


class EventModelTests(TestCase):
    def test_end_datetime_must_be_after_start_datetime(self):
        category = Category.objects.create(name="Workshops")
        event = Event(
            title="Broken Event",
            description="This should fail validation.",
            location="Library",
            start_datetime=timezone.now(),
            end_datetime=timezone.now() - timedelta(hours=1),
            category=category,
            contact_name="Alex",
            contact_email="alex@example.com",
        )

        with self.assertRaises(ValidationError):
            event.full_clean()


class EventSubmissionFormTests(TestCase):
    def test_invalid_end_datetime_is_rejected(self):
        category = Category.objects.create(name="Careers")
        start_datetime = timezone.now()
        form = EventSubmissionForm(
            data={
                "title": "Careers Night",
                "description": "Meet industry guests.",
                "location": "Student Hall",
                "start_datetime": start_datetime.strftime("%Y-%m-%dT%H:%M"),
                "end_datetime": (start_datetime - timedelta(minutes=30)).strftime(
                    "%Y-%m-%dT%H:%M"
                ),
                "category": category.pk,
                "contact_name": "Jordan",
                "contact_email": "jordan@example.com",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("end_datetime", form.errors)


class EventViewsTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Social", description="Fun campus events."
        )
        now = timezone.now()
        self.approved_event = Event.objects.create(
            title="Approved Event",
            description="Visible to the public.",
            location="Main Quad",
            start_datetime=now + timedelta(days=1),
            end_datetime=now + timedelta(days=1, hours=2),
            category=self.category,
            contact_name="Taylor",
            contact_email="taylor@example.com",
            is_approved=True,
        )
        self.pending_event = Event.objects.create(
            title="Pending Event",
            description="Hidden until approved.",
            location="Building A",
            start_datetime=now + timedelta(days=2),
            end_datetime=now + timedelta(days=2, hours=1),
            category=self.category,
            contact_name="Sam",
            contact_email="sam@example.com",
            is_approved=False,
        )

    def test_event_list_only_shows_approved_events(self):
        response = self.client.get(reverse("events_app:event_list"))
        self.assertContains(response, self.approved_event.title)
        self.assertNotContains(response, self.pending_event.title)

    def test_event_detail_returns_404_for_unapproved_event(self):
        response = self.client.get(
            reverse("events_app:event_detail", args=[self.pending_event.pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_event_create_submits_pending_event(self):
        start_datetime = timezone.now() + timedelta(days=3)
        response = self.client.post(
            reverse("events_app:event_create"),
            data={
                "title": "New Student Meetup",
                "description": "A welcome event for students.",
                "location": "Campus Cafe",
                "start_datetime": start_datetime.strftime("%Y-%m-%dT%H:%M"),
                "end_datetime": (start_datetime + timedelta(hours=1)).strftime(
                    "%Y-%m-%dT%H:%M"
                ),
                "category": self.category.pk,
                "contact_name": "Casey",
                "contact_email": "casey@example.com",
            },
            follow=True,
        )

        self.assertContains(response, "pending approval")
        self.assertTrue(
            Event.objects.filter(title="New Student Meetup", is_approved=False).exists()
        )

    def test_search_filters_approved_events(self):
        response = self.client.get(reverse("events_app:event_list"), {"q": "Approved"})
        self.assertContains(response, self.approved_event.title)
        self.assertNotContains(response, self.pending_event.title)

    def test_event_list_paginates_results(self):
        now = timezone.now()
        for index in range(6):
            Event.objects.create(
                title=f"Visible Event {index}",
                description="Shown on public pages.",
                location="Lecture Theatre",
                start_datetime=now + timedelta(days=5 + index),
                end_datetime=now + timedelta(days=5 + index, hours=1),
                category=self.category,
                contact_name="Morgan",
                contact_email=f"morgan{index}@example.com",
                is_approved=True,
            )

        response = self.client.get(reverse("events_app:event_list"), {"page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["page_obj"].has_previous())
