"""
WhatsApp webhook view for Mumbra Care.

Incoming messages are validated via Twilio's signature, parsed for intent,
then answered with real-time data fetched from the database.

Twilio sends a POST with form-encoded fields:
  Body     — the message text
  From     — sender's WhatsApp number  (whatsapp:+91XXXXXXXXXX)
  To       — our Twilio WhatsApp number

The view replies with TwiML (MessagingResponse).
"""

import logging
from functools import wraps

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse

from .models import BedStatus, Doctor, HealthcareFacility, Pharmacy
from .whatsapp_parser import parse_intent

logger = logging.getLogger(__name__)

# ── Twilio signature validation ───────────────────────────────────────────────

def _validate_twilio_signature(view_func):
    """Decorator: reject requests that don't carry a valid Twilio signature."""
    @wraps(view_func)
    def wrapped(self, request, *args, **kwargs):
        # In development (DEBUG=True) skip signature check so you can test
        # with curl/Postman without a real Twilio account.
        if settings.DEBUG:
            return view_func(self, request, *args, **kwargs)

        auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', '')
        if not auth_token:
            logger.error('TWILIO_AUTH_TOKEN not configured')
            return HttpResponseForbidden('Twilio auth token not configured')

        validator = RequestValidator(auth_token)
        signature = request.META.get('HTTP_X_TWILIO_SIGNATURE', '')
        url = request.build_absolute_uri()
        post_data = request.POST.dict()

        if not validator.validate(url, post_data, signature):
            logger.warning('Invalid Twilio signature from %s', request.META.get('REMOTE_ADDR'))
            return HttpResponseForbidden('Invalid Twilio signature')

        return view_func(self, request, *args, **kwargs)
    return wrapped


# ── Response builder helpers ──────────────────────────────────────────────────

_AREA_NAMES = {
    'KAUSA': 'Kausa',
    'AMRUT_NAGAR': 'Amrut Nagar',
    'STATION_ROAD': 'Station Road',
}

_SPECIALTY_NAMES = {
    'CARDIAC':   'Cardiac Expert',
    'PEDIATRIC': 'Pediatrician',
    'GENERAL':   'General Physician',
    'GYNAE':     'Gynaecologist',
    'ORTHO':     'Orthopaedic',
    'DERM':      'Dermatologist',
    'ENT':       'ENT Specialist',
}

HELP_MESSAGE = (
    "🏥 *Mumbra Care*\n\n"
    "Send a message like:\n"
    "• *bed* — see which hospitals have beds\n"
    "• *bed kausa* — beds in Kausa only\n"
    "• *doctor* — find a specialist\n"
    "• *cardiac doctor* — cardiologist near you\n"
    "• *pharmacy* — find a medical store\n"
    "• *night pharmacy* — 24/7 stores\n\n"
    "हिंदी: *बेड*, *डॉक्टर*, *दवाई* लिखें\n"
    "اردو: *بیڈ*، *ڈاکٹر*، *دوائی* لکھیں"
)

UNKNOWN_MESSAGE = (
    "Sorry, I didn't understand that. 🤔\n"
    "Send *help* to see what I can do."
)


def _twiml_response(body: str) -> HttpResponse:
    resp = MessagingResponse()
    resp.message(body)
    return HttpResponse(str(resp), content_type='application/xml')


def _bed_reply(area: str | None) -> str:
    qs = HealthcareFacility.objects.filter(is_active=True).select_related('bed_status')
    if area:
        qs = qs.filter(area=area)

    if not qs.exists():
        loc = _AREA_NAMES.get(area, 'your area')
        return f"No facilities found in {loc} right now."

    lines = [f"🏥 *Live Bed Status{' — ' + _AREA_NAMES[area] if area else ''}*\n"]
    for facility in qs[:10]:  # cap at 10 to keep message readable
        bs = getattr(facility, 'bed_status', None)
        if bs:
            avail = bs.available_beds
            total = bs.total_beds
            if avail == 0:
                icon = '🔴'
            elif avail / max(total, 1) <= 0.2:
                icon = '🟠'
            else:
                icon = '🟢'
            bed_line = f"{icon} *{facility.name}* — {avail}/{total} beds"
            if bs.icu_available > 0:
                bed_line += f" (ICU: {bs.icu_available})"
        else:
            bed_line = f"⚪ *{facility.name}* — no data"

        if facility.contact_number:
            bed_line += f"\n   📞 {facility.contact_number}"
        lines.append(bed_line)

    lines.append("\nReply *bed kausa* / *bed amrut* / *bed station* for a specific area.")
    return "\n".join(lines)


def _doctor_reply(area: str | None, specialty: str | None) -> str:
    qs = Doctor.objects.select_related('facility').filter(is_available=True)
    if area:
        qs = qs.filter(facility__area=area)
    if specialty:
        qs = qs.filter(specialty=specialty)

    if not qs.exists():
        spec_name = _SPECIALTY_NAMES.get(specialty, 'Doctor')
        loc = _AREA_NAMES.get(area, '')
        qualifier = f"{spec_name}{' in ' + loc if loc else ''}"
        return f"No {qualifier} available right now. Please try again later."

    title_parts = ['👨‍⚕️ *Doctors In Clinic Now*']
    if specialty:
        title_parts.append(f"({_SPECIALTY_NAMES.get(specialty, specialty)})")
    if area:
        title_parts.append(f"— {_AREA_NAMES[area]}")
    lines = [' '.join(title_parts) + '\n']

    for doc in qs[:8]:
        line = f"✅ *Dr. {doc.name}*"
        line += f"\n   {_SPECIALTY_NAMES.get(doc.specialty, doc.specialty)}"
        line += f"\n   🏥 {doc.facility.name}"
        if doc.contact_number:
            line += f"\n   📞 {doc.contact_number}"
        lines.append(line)

    lines.append("\nReply *cardiac doctor* / *pediatric doctor* etc. for specialists.")
    return "\n".join(lines)


def _pharmacy_reply(area: str | None, night_only: bool = False) -> str:
    qs = Pharmacy.objects.filter(is_active=True)
    if area:
        qs = qs.filter(area=area)
    if night_only:
        qs = qs.filter(is_24_7=True)

    if not qs.exists():
        return "No pharmacies found. Try without an area filter."

    loc = _AREA_NAMES.get(area, '')
    lines = [f"💊 *Pharmacies{' — ' + loc if loc else ''}*\n"]

    for ph in qs[:8]:
        icon = '🕐' if ph.is_24_7 else '🏪'
        line = f"{icon} *{ph.name}*"
        if ph.is_24_7:
            line += ' _(24 / 7)_'
        elif ph.opening_time and ph.closing_time:
            line += f' _{ph.opening_time.strftime("%-H:%M")}–{ph.closing_time.strftime("%-H:%M")}_'
        line += f"\n   📍 {ph.address}"
        if ph.contact_number:
            line += f"\n   📞 {ph.contact_number}"
        lines.append(line)

    lines.append("\nReply *night pharmacy* for 24/7 stores only.")
    return "\n".join(lines)


# ── Webhook View ──────────────────────────────────────────────────────────────

@method_decorator(csrf_exempt, name='dispatch')
class WhatsAppWebhookView(View):
    """POST /api/whatsapp/webhook/ — Twilio WhatsApp inbound handler."""

    @_validate_twilio_signature
    def post(self, request):
        body = request.POST.get('Body', '').strip()
        sender = request.POST.get('From', '')
        logger.info('WhatsApp message from %s: %r', sender, body[:120])

        if not body:
            return _twiml_response(HELP_MESSAGE)

        intent_data = parse_intent(body)
        intent = intent_data['intent']
        area = intent_data['area']
        specialty = intent_data['specialty']

        # Detect "night pharmacy" pattern specifically
        night_pharmacy = 'night' in body.lower() or 'रात' in body or 'رات' in body

        if intent == 'HELP':
            reply = HELP_MESSAGE
        elif intent == 'BED':
            reply = _bed_reply(area)
        elif intent == 'DOCTOR':
            reply = _doctor_reply(area, specialty)
        elif intent == 'PHARMACY':
            reply = _pharmacy_reply(area, night_only=night_pharmacy)
        else:
            reply = UNKNOWN_MESSAGE

        return _twiml_response(reply)
