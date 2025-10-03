from events.models import Event
from django.forms import ModelForm
from django.forms.widgets import Textarea, TextInput, SelectMultiple, Select, FileInput, DateInput, TimeInput
from django.core.exceptions import ValidationError

class CreateEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["title", "date", "start_time", "end_time", "place", "image", "status", "detail", "categories"]
        widgets = {
            "title": TextInput(attrs={"class": "text-black border rounded-lg px-3 py-2 w-full"}),
            "detail": Textarea(attrs={"rows": 5, "class": "text-black border resize-none rounded-lg px-3 py-2 w-full"}),
            "place": TextInput(attrs={"class": "text-black border rounded-lg px-3 py-2 w-full"}),
            "date": DateInput(attrs={"class": "text-black border rounded-lg px-3 py-2 w-full", "type": "date"}),
            "start_time": TimeInput(attrs={"class": "text-black border rounded-lg px-3 py-2 w-full", "type": "time"}),
            "end_time": TimeInput(attrs={"class": "text-black border rounded-lg px-3 py-2 w-full", "type": "time"}),
            "status": Select(attrs={"class": "text-black border rounded-lg px-3 py-2 w-full cursor-pointer"}),
            "categories": SelectMultiple(attrs={"class": "text-black border rounded-lg px-3 py-2 w-full"}),
            "image": FileInput(attrs={"class": "text-black hidden"})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) #สร้าง form ปกติ (ดึง fields จาก model มา)
        self.fields["status"].choices = [ #เข้าถึง field status ที่ Django สร้างให้
            (Event.StatusEvent.DRAFT, "Draft"),
            (Event.StatusEvent.UPCOMING, "Upcoming")
        ]
    
    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date <= date.today():
            raise ValidationError("Please select a date later than today.")
        return date

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time and end_time < start_time:
            raise ValidationError("End time cannot be before start time")