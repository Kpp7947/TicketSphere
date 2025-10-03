from tickets.models import TicketType
from django.forms import ModelForm
from django.forms.widgets import TextInput, NumberInput, CheckboxInput
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory

class CreateTicketTypeForm(ModelForm):
    # name = forms.CharField(required=False)
    class Meta:
        model = TicketType
        fields = ["name", "price", "quantity", "is_unlimited"]
        widgets = {
            "name": TextInput(attrs={"class": "border rounded-lg px-3 py-2 w-full"}),
            "price": NumberInput(attrs={"class": "border rounded-lg px-3 py-2 w-full"}),
            "quantity": NumberInput(attrs={"class": "border rounded-lg px-3 py-2 w-full"}),
            "is_unlimited": CheckboxInput(attrs={"class": "border rounded-lg px-3 py-2 w-full"})
        }

    def clean(self):
        cleaned_data = super().clean()
        is_unlimited = cleaned_data.get("is_unlimited")
        quantity = cleaned_data.get("quantity")
        
        if not cleaned_data.get("DELETE"):
            if not cleaned_data.get("name"):
                raise ValidationError("Please enter ticket name.")

        if is_unlimited:
            cleaned_data["quantity"] = 0
        else:
            if quantity is None or quantity <= 0:
                raise ValidationError("Ticket quantity must be greater than 0 if not Unlimited.")
        return cleaned_data

TicketFormSet = modelformset_factory(
    TicketType,
    form=CreateTicketTypeForm,
    extra=0,
    can_delete=True,
    min_num=1,
    validate_min=1
)