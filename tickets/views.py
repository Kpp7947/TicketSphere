from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from .forms import TicketFormSet
from .models import *
from register.models import Register
from django.template.loader import render_to_string
import qrcode
import uuid
from datetime import timedelta
from io import BytesIO
from django.core.files.base import ContentFile
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Create your views here.
class AddTicketFormView(PermissionRequiredMixin, View):
    # ให้เฉพาะเจ้าของ(organizer) เท่านั้นที่เพิ่มได้
    permission_required = ["events.add_event", "tickets.add_tickettype"]
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
    
def generate_qr_code(register, date):
    exp = date+timedelta(days=1)
    ticket_code = str(uuid.uuid4())
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(ticket_code)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    file_name = f"{ticket_code}.png"
    qr_file = ContentFile(buffer.getvalue(), file_name)

    ticket = Ticket.objects.create(
        register=register,
        ticket_code=ticket_code,
        expired_at=exp
    )
    ticket.qr_code.save(file_name, qr_file)
    return ticket

class TicketDetail(View):
    # ให้เฉพาะเจ้าของ(user) ticket เท่านั้นที่ดูได้
    # permission_required = ["tickets.view_ticket"]
    def get(self, request, id):
        register = Register.objects.get(id=id)
        ticket = Ticket.objects.filter(
            register=register
        )
        return render(request, "ticket_detail.html", {
            "ticket": ticket
        })