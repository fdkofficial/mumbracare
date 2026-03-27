"""
WhatsApp message intent parser for Mumbra Care.

Understands queries in English, Hindi and Urdu without any ML dependency.
Returns a structured intent dict that the webhook view uses to build a reply.
"""

import re

# ── Intent keyword maps (lowercase) ──────────────────────────────────────────

_BED_KEYWORDS = {
    # English
    'bed', 'beds', 'admit', 'admission', 'hospital', 'hospitals', 'icu',
    'room', 'ward', 'available',
    # Hindi
    'बेड', 'अस्पताल', 'भर्ती', 'उपलब्ध',
    # Urdu
    'بیڈ', 'اسپتال', 'داخلہ', 'دستیاب',
}

_DOCTOR_KEYWORDS = {
    # English
    'doctor', 'dr', 'doc', 'specialist', 'physician', 'cardiac', 'heart',
    'pediatric', 'child', 'children', 'gynaecologist', 'gynae', 'ortho',
    'ent', 'dermatologist', 'skin', 'general',
    # Hindi
    'डॉक्टर', 'चिकित्सक', 'विशेषज्ञ', 'हड्डी', 'बच्चा', 'बच्चे', 'त्वचा',
    # Urdu
    'ڈاکٹر', 'معالج', 'ماہر', 'بچے', 'دل',
}

_PHARMACY_KEYWORDS = {
    # English
    'pharmacy', 'medical', 'medicine', 'drug', 'chemist', 'store', 'shop',
    'open', 'night', 'late', '24', '24/7',
    # Hindi
    'दवा', 'दवाई', 'मेडिकल', 'फार्मेसी', 'रात',
    # Urdu
    'دوائی', 'دوا', 'میڈیکل', 'فارمیسی', 'رات',
}

_AREA_MAP = {
    'kausa':        'KAUSA',
    'कौसा':         'KAUSA',
    'کوسہ':         'KAUSA',
    'amrut':        'AMRUT_NAGAR',
    'amrut nagar':  'AMRUT_NAGAR',
    'अमृत':         'AMRUT_NAGAR',
    'امرت':         'AMRUT_NAGAR',
    'station':      'STATION_ROAD',
    'station road': 'STATION_ROAD',
    'स्टेशन':       'STATION_ROAD',
    'اسٹیشن':       'STATION_ROAD',
}

_SPECIALTY_MAP = {
    'cardiac': 'CARDIAC', 'heart': 'CARDIAC',
    'दिल': 'CARDIAC', 'قلب': 'CARDIAC',
    'pediatric': 'PEDIATRIC', 'child': 'PEDIATRIC', 'children': 'PEDIATRIC',
    'बच्चा': 'PEDIATRIC', 'بچے': 'PEDIATRIC',
    'gynae': 'GYNAE', 'gynecologist': 'GYNAE', 'gynaecologist': 'GYNAE',
    'ortho': 'ORTHO', 'bone': 'ORTHO', 'हड्डी': 'ORTHO',
    'ent': 'ENT',
    'derm': 'DERM', 'skin': 'DERM', 'त्वचा': 'DERM',
    'general': 'GENERAL',
}

_HELP_KEYWORDS = {
    'help', 'hi', 'hello', 'start', 'menu', 'हेल्प', 'मदद', 'ہیلپ', 'مدد',
    'السلام', 'नमस्ते', 'हैलो',
}


def parse_intent(message: str) -> dict:
    """Return ``{'intent': str, 'area': str|None, 'specialty': str|None}``."""
    text = message.strip().lower()
    words = set(re.split(r'[\s,،।]+', text))

    # Detect area
    area = None
    for phrase, code in _AREA_MAP.items():
        if phrase in text:
            area = code
            break

    # Detect specialty
    specialty = None
    for kw, code in _SPECIALTY_MAP.items():
        if kw in text:
            specialty = code
            break

    # Detect intent
    if words & _HELP_KEYWORDS and len(words) <= 3:
        return {'intent': 'HELP', 'area': area, 'specialty': None}
    if words & _BED_KEYWORDS:
        return {'intent': 'BED', 'area': area, 'specialty': None}
    if words & _DOCTOR_KEYWORDS:
        return {'intent': 'DOCTOR', 'area': area, 'specialty': specialty}
    if words & _PHARMACY_KEYWORDS:
        return {'intent': 'PHARMACY', 'area': area, 'specialty': None}

    return {'intent': 'UNKNOWN', 'area': area, 'specialty': None}
