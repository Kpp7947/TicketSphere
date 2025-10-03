from django.db import models
# from events.models import Event
# from tickets.models import TicketType
from django.contrib.auth.models import User

# Create your models here.
class Register(models.Model):
    class StatusRegister(models.TextChoices):
        REGISTERED = "registered", "Registered"
        CANCELLED = "cancelled", "Cancelled"
        ATTENDED  = "attended", "Attended"
        NOSHOW  = "no_show", "No show"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE)
    ticket_type = models.ForeignKey("tickets.TicketType", on_delete=models.CASCADE)
    status = models.CharField(
        choices=StatusRegister.choices,
        default=StatusRegister.REGISTERED
    )
    registered_at = models.DateTimeField(auto_now_add=True)

