from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from .forms import TicketFormSet
from .models import *
from django.template.loader import render_to_string
# Create your views here.
class AddTicketFormView(View):
    def get(self, request):
        index = request.GET.get("index")
        print("index:", index)
        if index is None:
            return HttpResponseBadRequest("index required")
        # สร้าง empty_form แล้วสลับ prefix ให้เป็น form-<index>
        # TicketFormSet = modelformset_factory(Ticket, form=TicketForm, can_delete=True, extra=0)
        dummy = TicketFormSet(queryset=TicketType.objects.none(), prefix="form")
        empty = dummy.empty_form
        empty.prefix = f"form-{index}"

        html = render_to_string("partials/ticket_form.html", {"form": empty}, request=request)
        # แถมสคริปต์เล็ก ๆ ให้อัปเดต TOTAL_FORMS
        html += "<script>document.getElementById('id_form-TOTAL_FORMS').value = Number(document.getElementById('id_form-TOTAL_FORMS').value)+1;</script>"
        return HttpResponse(html)