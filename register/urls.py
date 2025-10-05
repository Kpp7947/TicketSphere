from django.urls import path

from . import views

urlpatterns = [
   path('myprofile/', views.UserProfileEventView.as_view(), name="user-profile-event-registered"),
   path('registered/<int:id>', views.CreateRegisterationTicket.as_view(), name="user-registered-event"),
]