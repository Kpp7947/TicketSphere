from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login, update_session_auth_hash
from .forms import CustomUserCreationForm, CustomPasswordChangeForm
from django.contrib.auth.models import Group
from register.models import Register
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if request.user.groups.exclude(name__in=("Viewer", "User")):
                return redirect("organizer-home")
            else:
                return redirect("user-home")
        return render(request, "login.html", {"form": form})
    
class SignupView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        # print(form)
        return render(request, "signup.html", {"form": form})
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        print(form.errors)
        if form.is_valid():
            print("yes")
            form.save()
            print("yes")
            return redirect("login")
        print("no")
        return render(request, "signup.html", {"form": form})
    
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

@method_decorator(login_required, name='dispatch') #dispatch() จะตัดสินใจว่า request เป็น GET หรือ POST แล้วเรียก method ที่เหมาะสม
class UpdateUserProfile(View):
    def get(self, request):
        page = request.GET.get("page", "")
        userform = CustomUserCreationForm(instance=request.user)        
        return render(request, "myaccount.html", {
            "userform": userform,
            "page": page
        })
    
    def post(self, request):
        userform = CustomUserCreationForm(data=request.POST)
        print(userform)
    
class ChangePassword(View):
    def get(self, request):
        page = request.GET.get("page", "")
        passform = CustomPasswordChangeForm(user=request.user)
        return render(request, "myaccount.html", {
            "passform": passform,
            "page": page
        })
    
    def post(self, request):
        passform = CustomPasswordChangeForm(user=request.POST)