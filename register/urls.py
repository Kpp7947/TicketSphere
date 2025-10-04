from django.urls import path

from . import views

urlpatterns = [
   path('myevent/', views.UserEventView.as_view(), name="user-event"),
   path('registered/<int:id>', views.CreateRegisterationTicket.as_view(), name="user-registered-event"),
]