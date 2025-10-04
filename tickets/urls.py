from django.urls import path

from . import views

urlpatterns = [
    path("add_ticket_form/", views.AddTicketFormView.as_view(), name="add_ticket_form"),
]