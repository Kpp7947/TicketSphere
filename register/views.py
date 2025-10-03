from django.shortcuts import render
from django.views import View
from .models import Register
# Create your views here.
class UserEventView(View):
    def get(self, request):
        page = request.GET.get("page", "")
        result = Register.objects.filter(
            user=request.user.id
        )
        return render(request, "myaccount.html", {
            "result": result,
            "page": page
        })