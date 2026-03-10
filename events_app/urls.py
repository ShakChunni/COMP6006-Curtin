from django.urls import path

from . import views

app_name = "events_app"

urlpatterns = [
    path("", views.event_list, name="home"),
    path("events/", views.event_list, name="event_list"),
    path("events/create/", views.event_create, name="event_create"),
    path("events/<int:event_id>/", views.event_detail, name="event_detail"),
    path("categories/", views.category_list, name="category_list"),
    path(
        "categories/<int:category_id>/", views.category_events, name="category_events"
    ),
]
