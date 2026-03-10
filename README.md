# Campus Events Directory

This project is a Django web application for browsing campus events and submitting new events for admin approval.

## Features

- Public event submission form with CSRF protection.
- Admin-managed event categories.
- Moderation workflow for all submitted events.
- Approved-only public listings and detail pages.
- Category pages for approved events.
- Search across approved events.
- Pagination for public event listings.
- Custom 404 and 500 templates.

## Project Structure

- `campus_events/`: project settings and root URL configuration.
- `events_app/`: models, form, views, admin configuration, tests, and routes.
- `templates/`: project templates, including error pages.

## Setup

Use the existing virtual environment for this workspace.

```bash
cd /Users/ashfaq/Studies/COMP6006/assignment1
/Users/ashfaq/Studies/COMP6006/.venv/bin/python manage.py migrate
```

## Run The Server

```bash
cd /Users/ashfaq/Studies/COMP6006/assignment1
/Users/ashfaq/Studies/COMP6006/.venv/bin/python manage.py runserver
```

Open `http://127.0.0.1:8000/` to view approved events.

## Create A Superuser

```bash
cd /Users/ashfaq/Studies/COMP6006/assignment1
/Users/ashfaq/Studies/COMP6006/.venv/bin/python manage.py createsuperuser
```

Then sign in at `http://127.0.0.1:8000/admin/`.

## Moderation Workflow

1. A visitor submits an event from the public form.
2. The event is saved with `is_approved=False`.
3. The event does not appear on public listings or detail pages.
4. An admin approves the event in Django admin.
5. Once approved, the event becomes visible on the public pages.

## Search And Pagination

- The main approved events page supports keyword search.
- Category event pages also support keyword search within that category.
- Public event listings are paginated with 5 events per page.

## Validation

- Required fields are enforced through the Django form.
- `contact_email` uses Django's email validation.
- `end_datetime` must be later than `start_datetime`.

## Custom Error Pages

Custom 404 and 500 pages are included.

To test them locally, set `DEBUG = False` in `campus_events/settings.py` and run the server with the existing `ALLOWED_HOSTS` values.

## Run Tests

```bash
cd /Users/ashfaq/Studies/COMP6006/assignment1
/Users/ashfaq/Studies/COMP6006/.venv/bin/python manage.py test
```

## Notes

- Categories are created and maintained through the Django admin panel.
- Public users cannot approve events.
- The declaration of originality should be written and signed by the submitting student.
