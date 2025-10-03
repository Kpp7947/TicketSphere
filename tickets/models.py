from django.db import models
# from events.models import Event
# from register.models import Register

# Create your models here.
class TicketType(models.Model):
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, related_name="ticket_types")
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    is_unlimited = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    class StatusTicket(models.TextChoices):
        VALID = "valid", "Valid"
        USED = "used", "Used"
        EXPIRED = "expired", "Expired"
    register = models.ForeignKey("register.Register", on_delete=models.CASCADE)
    ticket_code = models.CharField(max_length=100)
    qr_code = models.CharField(max_length=100)
    status = models.CharField(
        choices=StatusTicket.choices,
        default=StatusTicket.VALID
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)