from django.shortcuts import render

from .models import Event, Category
from register.models import Register
from tickets.models import TicketType
from decimal import Decimal

from django.shortcuts import render, redirect
from django.views import View
from events.forms import CreateEventForm
# from django.forms import modelformset_factory
# from .models import *
# from .forms import TicketFormSet
import json
# from datetime import date, datetime
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.db.models import Count, F, Q, Sum
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from tickets.forms import TicketFormSet
# Create your views here.

class HomeView(View):
    
    def get(self, request):
        event_list = Event.objects.filter(
            status="upcoming"
        )
        category = Category.objects.all()
        return render(request, "index.html", {
            "event_list": event_list,
            "category": category
        })
    
class SearchView(View):
    def get(self, request):
        search = request.GET.get("q", "")
        event = Event.objects.filter(status="upcoming")
        if search:
            event = event.filter(
                Q(title__icontains=search) | 
                Q(place__icontains=search) | 
                Q(categories__name__icontains=search)
            )
        # print(event)
        return render(request, "search_event.html", {
            "search": search,
            "events": event,
            "total": event.count()
        })

class EventDetail(View):
    def get(self, request, id):
        event = Event.objects.get(id=id)
        user = request.user
        register = Register.objects.filter(user=user.id, event=event)
        # print(register)

        ticket = TicketType.objects.filter(event=event).annotate(
            amount=F('quantity') - Count('register')
        )

        return render(request, "event_detail.html", {
            "event": event,
            "ticket": ticket,
            "register": register
        })


# Organizer
class OrganizerHomeView(PermissionRequiredMixin, View):
    permission_required = ["events.view_event"]
    def get(self, request):
        search = request.GET.get("search", "")
        price_filter = request.GET.get("price", "")
        category_filter = request.GET.get("category", "")
        # print("user: ", request.user.groups.all())
        user = request.user.groups.exclude(name__in=("Viewer", "User"))
        # print(user)
        new_price_filter = None
        new_cat_filter = None

        if "-" in price_filter:
            new_price_filter = price_filter.split("-")

        if category_filter:
            new_cat_filter = category_filter.split(",")
        
        event_list = Event.objects.prefetch_related("categories", "ticket_types").all().order_by("-created_at")

        # print(new_price_filter)
        # print(price_filter)

        if search != "":
            event_list = event_list.filter(
                title__icontains=search
            )

        if new_cat_filter:
            event_list = event_list.filter(
                categories__name__in=new_cat_filter
            )
        
        if new_price_filter:
            event_list = event_list.filter(
                ticket_types__price__range=(Decimal(new_price_filter[0]), Decimal(new_price_filter[1]))
            )
        else:
            if price_filter == "0":
                event_list = event_list.filter(
                    ticket_types__price=(Decimal(price_filter))
                )
            elif price_filter == "10000":
                event_list = event_list.filter(
                    ticket_types__price__gt=(Decimal(price_filter))
                )
        event_list = event_list.distinct()
        category = Category.objects.all()


        for event in event_list:
            event.category_name = [cat.name for cat in event.categories.all()]
            event.ticket_name = [tic.name for tic in event.ticket_types.all()] 
        # print(event_list[2].category_name) => list
        return render(request, "organizer/home.html", {
            "event_list": event_list,
            "total": event_list.count(),
            "category": category,
            "search": search,
            "price_filter": price_filter,
            "category_filter": category_filter
        })
    
class CreateEvent(View):
    def get(self, request):
        eventForm = CreateEventForm()
        # user = User.objects.get(id=1)
        # print("user: ", user)
        ticketForm = TicketFormSet(queryset=TicketType.objects.none())
        return render(request, "organizer/create_event.html", {
            "eventForm": eventForm, 
            "ticketForm": ticketForm
        })
    
    def post(self, request):
        # event = Event.objects
        event_form = CreateEventForm(request.POST, request.FILES)
        ticket_form = TicketFormSet(request.POST)
        # user = User.objects.get(id=1)
        user = request.user
        # print(user)
        try:
            with transaction.atomic():
                if event_form.is_valid():
                    event = event_form.save(commit=False)
                    event.user = user
                    event.save()
                    if ticket_form.is_valid():
                        tickets = ticket_form.save(commit=False)
                        for ticket in tickets:
                            ticket.event = event
                            ticket.save()
                        return redirect('organizer-home')
            raise transaction.TransactionManagementError("Error")
        except Exception as e:
            print(e)
        return render(request, "organizer/create_event.html", {
                "eventForm": event_form, 
                "ticketForm": ticket_form
            })
    
class OrganizerEventDetail(View):
    def get(self, request, id):
        event_detail = Event.objects.get(pk=id)
        ticket = TicketType.objects.filter(event=event_detail).annotate(
            registered=Count('register'),
            amount=F('quantity') - Count('register')
        )
        total = TicketType.objects.filter(event=event_detail).aggregate(
            registered=Count('register')
        )
        # print(total)
        # print(event_detail)
        # print(ticket)
        # print(event_detail.register_set.all())
        return render(request, "organizer/org_event_detail.html", {
            "event": event_detail,
            "ticket": ticket,
            "total": total['registered']
        })

class OrganizerUpdateEvent(View):
    def get(self, request, id):
        event_detail = Event.objects.get(pk=id)
        ticket = TicketType.objects.filter(event=event_detail)
        # print("ticket: ", ticket)

        event_form = CreateEventForm(instance=event_detail)
        ticket_form = TicketFormSet(queryset=ticket)
        return render(request, "organizer/update_event.html", {
            "eventForm": event_form, 
            "ticketForm": ticket_form
        })
    
    def post(self, request, id):
        event_detail = Event.objects.get(id=id)
        tickettype = TicketType.objects.filter(event=event_detail)

        event_form = CreateEventForm(request.POST, request.FILES, instance=event_detail)
        ticket_form = TicketFormSet(request.POST, queryset=tickettype)
        # ticket_form = TicketFormSet(request.POST)
        # print(ticket_form)

        if event_form.is_valid() and ticket_form.is_valid():
            event = event_form.save()
            tickets = ticket_form.save(commit=False)
            for obj in ticket_form.deleted_objects:
                obj.delete()
            for ticket in tickets:
                ticket.event = event
                ticket.save()
            # event_form.save()
            # ticket_form.save()
            return redirect("organizer-event-detail", id)
        
        return render(request, "organizer/update_event.html", {
            "eventForm": event_form, 
            "ticketForm": ticket_form
        })