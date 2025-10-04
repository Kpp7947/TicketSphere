from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Register
from events.models import Event
from tickets.models import TicketType, Ticket
from django.contrib import messages
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
    
class CreateRegisterationTicket(View):
    def post(self, request, id):
        event = get_object_or_404(Event, id=id)
        ticket_id = request.POST.get("ticket_type")

        if not ticket_id:
            messages.error(request, "Please select a ticket.")
            return redirect("user-event-detail", id=id)
        
        if Register.objects.exclude(user=request.user, event=event).exists():
            messages.error(request, "You have already registered for this event.")
            return redirect("user-event-detail", id=id)
        
        ticket_type = get_object_or_404(TicketType, id=ticket_id)
        
        # registered = Register.objects.create(
        #     user=request.user,
        #     event=event,
        #     ticket_type=ticket_type
        # )
        print(id)
        print(ticket_id)