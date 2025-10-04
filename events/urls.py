from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="user-home"),
    path("event/", views.SearchView.as_view(), name="search-event"),
    path("event_detail/<int:id>", views.EventDetail.as_view(), name="user-event-detail"),
    path("organizer/home", views.OrganizerHomeView.as_view(), name="organizer-home"),
    path("organizer/create_event/", views.CreateEvent.as_view(), name="create-event"),
    path("organizer/event_detail/<int:id>", views.OrganizerEventDetail.as_view(), name="organizer-event-detail"),
    path("organizer/update_event/<int:id>", views.OrganizerUpdateEvent.as_view(), name="organizer-update-event"),
]