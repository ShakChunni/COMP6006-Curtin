from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EventSubmissionForm
from .models import Category, Event


EVENTS_PER_PAGE = 5


def _get_search_query(request):
    return request.GET.get("q", "").strip()


def _filter_events(queryset, search_query):
    if not search_query:
        return queryset
    return queryset.filter(
        Q(title__icontains=search_query)
        | Q(description__icontains=search_query)
        | Q(location__icontains=search_query)
        | Q(category__name__icontains=search_query)
    )


def event_list(request):
    search_query = _get_search_query(request)
    events = Event.objects.filter(is_approved=True).select_related("category")
    events = _filter_events(events, search_query)
    paginator = Paginator(events, EVENTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "events_app/event_list.html",
        {"page_obj": page_obj, "search_query": search_query},
    )


def event_detail(request, event_id):
    event = get_object_or_404(
        Event.objects.select_related("category"),
        pk=event_id,
        is_approved=True,
    )
    return render(request, "events_app/event_detail.html", {"event": event})


def event_create(request):
    if request.method == "POST":
        form = EventSubmissionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your event was submitted successfully and is now pending approval.",
            )
            return redirect("events_app:event_create")
    else:
        form = EventSubmissionForm()

    return render(request, "events_app/event_create.html", {"form": form})


def category_list(request):
    categories = Category.objects.all()
    return render(request, "events_app/category_list.html", {"categories": categories})


def category_events(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    search_query = _get_search_query(request)
    events = category.events.filter(is_approved=True).select_related("category")
    events = _filter_events(events, search_query)
    paginator = Paginator(events, EVENTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "events_app/category_events.html",
        {"category": category, "page_obj": page_obj, "search_query": search_query},
    )


def custom_404(request, exception):
    return render(request, "404.html", status=404)


def custom_500(request):
    return render(request, "500.html", status=500)
