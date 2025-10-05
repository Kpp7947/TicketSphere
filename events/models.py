from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=10, default="#FFFFFF")

    def __str__(self):
        return self.name

class Event(models.Model):
    class StatusEvent(models.TextChoices):
        DRAFT = "draft", "Draft"
        UPCOMING = "upcoming", "Upcoming"
        ONGOING = "ongoing", "Ongoing"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    place = models.CharField(max_length=255)
    image = models.ImageField(upload_to="image/events/", blank=True, default="image/events/Coming_soon.jpg")
    detail = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=StatusEvent.choices,
        default=StatusEvent.DRAFT
    )
    categories = models.ManyToManyField(Category, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
