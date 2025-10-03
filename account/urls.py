from django.urls import path

from . import views

urlpatterns = [
    path("", views.LoginView.as_view(), name="login"),
    path("signup/", views.SignupView.as_view(), name="sign-up"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('myprofile/', views.UpdateUserProfile.as_view(), name="user-profile"),
    path('changepass/', views.ChangePassword.as_view(), name="user-changepass"),
]