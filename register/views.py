from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Register
from events.models import Event
from tickets.models import TicketType, Ticket
from django.contrib import messages
from django.db import transaction
from tickets.views import generate_qr_code
from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
@method_decorator(login_required, name='dispatch')
class UserProfileEventView(View):
    # ให้เฉพาะเจ้าของ(user) เท่านั้นที่ดูได้ => login
    def get(self, request):
        page = request.GET.get("page", "")
        result = Register.objects.filter(
            user=request.user.id
        )
        return render(request, "myaccount.html", {
            "result": result,
            "page": page
        })


class CreateRegisterationTicket(PermissionRequiredMixin, View):
    # user ที่ login
    permission_required = ["register.add_register", "tickets.add_ticket"]
    def post(self, request, id):
        event = get_object_or_404(Event, id=id)
        ticket_id = request.POST.get("ticket_type")

        if not ticket_id:
            messages.error(request, "Please select a ticket.")
            return redirect("user-event-detail", id=id)
        
        if Register.objects.filter(user=request.user, event=event).exists():
            messages.error(request, "You have already registered for this event.")
            return redirect("user-event-detail", id=id)
        
        ticket_type = get_object_or_404(TicketType, id=ticket_id)
        # print(event.date + timedelta(days=1))

        try:
            with transaction.atomic():
                register = Register.objects.create(
                    user=request.user,
                    event=event,
                    ticket_type=ticket_type
                )
                generate_qr_code(register, event.date)
                return redirect("user-event-detail", id=id)
            raise transaction.TransactionManagementError("Error")
        except Exception as e:
            print(e)
            return redirect("user-event-detail", id=id)
