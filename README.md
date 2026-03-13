# Campus Events Directory (Assignment 1)

I built this Django web application for Assignment 1 of COMP6006. It allows public users to browse approved campus events and submit new events for admin approval.

This submission contains one folder: `234722097_assignment1`.

## What I Covered

- Project: `campus_events`
- App: `events_app`
- Models: `Category` and `Event`
- Moderation workflow with `is_approved` and `approved_at`, timezone set to Perth, WA.
- Public event submission form
- Approved-only event list and event detail pages
- Category list and category event pages
- Custom `404` and `500` error pages
- Basic search, pagination, validation, and admin moderation support

## Requirements

- Python 3.10+
- Django

## Optional Virtual Environment

I recommend using a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install django
```

## Run the Project

From inside the `assignment1` folder:

```bash
python manage.py migrate
python manage.py runserver
```

Open: `http://127.0.0.1:8000/`

## Create Admin User

```bash
python manage.py createsuperuser
```

Then log in at: `http://127.0.0.1:8000/admin/`

## Moderation Flow

1. A user submits an event through `/events/create/`.
2. The event is saved as pending (`is_approved=False`).
3. Pending events are not visible on public pages.
4. I approve events in Django admin by setting `is_approved=True`.
5. Approved events become visible in public listings and detail pages.

## Security and Validation

- CSRF token is included in the event submission form.
- `get_object_or_404()` is used for safe event detail retrieval.
- Email is validated with `EmailField`.
- `end_datetime` must be later than `start_datetime`.

## Test Commands

```bash
python manage.py test
python manage.py check
```

## Viewing Custom 404 and 500 Pages

During development, Django shows a technical debug error page when `DEBUG=True`.
To see my custom `404.html` and `500.html` templates:

1. Open `campus_events/settings.py` and set `DEBUG = False`.
2. Keep `ALLOWED_HOSTS` set for local use (for example: `127.0.0.1`, `localhost`).
3. Run the server:

```bash
python manage.py runserver
```

4. Test custom 404 by visiting a missing URL, for example:
	- `http://127.0.0.1:8000/categories/9999/`
5. Test custom 500 by temporarily raising an exception in a view, then reload that page.

After testing, set `DEBUG = True` again for normal development.
