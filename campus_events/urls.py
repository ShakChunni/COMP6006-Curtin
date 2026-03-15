from django.contrib import admin
from django.urls import include, path

handler404 = "events_app.views.custom_404"
handler500 = "events_app.views.custom_500"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("events_app.urls")),
]
