from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login, update_session_auth_hash
from .forms import CustomUserCreationForm, CustomPasswordChangeForm, CustomUserChangeForm
from django.contrib.auth.models import Group
from register.models import Register
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
# Create your views here.

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() #ดึง user object ที่ผ่านการตรวจสอบแล้ว จาก AuthenticationForm
            login(request, user)
            # print(user.groups.all())
            # if user.groups.filter(name__in=["Organizer"]).exists(): #"Organizer" → string("Organizer") → string("Organizer",) → tuple ✅["Organizer"] → list ✅
                # print("yess")
                # return redirect("organizer-home")
            if user.groups.filter(name__in=["Admin"]).exists() or user.is_staff:
                return redirect("/admin/")
            else:
                return redirect("user-home")
        return render(request, "login.html", {"form": form})
    
class SignupView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "signup.html", {"form": form})
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        organizer = request.POST.get("organizer")
        organizer_group = Group.objects.get(name="Organizer")
        user_group = Group.objects.get(name="User")
        if form.is_valid():
            user = form.save()
            user.groups.add(user_group)
            if organizer is not None:
                user.groups.add(organizer_group)
            return redirect("login")
        return render(request, "signup.html", {"form": form})
    
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

@method_decorator(login_required, name='dispatch') #dispatch() จะตัดสินใจว่า request เป็น GET หรือ POST แล้วเรียก method ที่เหมาะสม
class UpdateUserProfile(View):
    def get(self, request):
        page = request.GET.get("page", "")
        userform = CustomUserChangeForm(instance=request.user)        
        return render(request, "myaccount.html", {
            "userform": userform,
            "page": page
        })
    
    def post(self, request):
        page = request.GET.get("page", "")
        userform = CustomUserChangeForm(request.POST, instance=request.user)
        if userform.is_valid():
            userform.save()
            return redirect('user-profile')
        return render(request, "myaccount.html", {
            "userform": userform,
            "page": page
        })

@method_decorator(login_required, name='dispatch')
class ChangePassword(View):
    def get(self, request):
        page = request.GET.get("page", "")
        passform = CustomPasswordChangeForm(request.user)
        return render(request, "myaccount.html", {
            "passform": passform,
            "page": page
        })
    
    def post(self, request):
        page = request.GET.get("page", "")
        passform = CustomPasswordChangeForm(request.user, request.POST)
        if passform.is_valid():
            user = passform.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully!")
            return redirect('user-profile')
        # print(passform.errors)
        return render(request, "myaccount.html", {
            "passform": passform,
            "page": page
        })