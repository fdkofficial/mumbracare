"""
Management command: seed_data

Populates the database with real-world-representative healthcare facilities,
doctors, bed statuses, and pharmacies for the Mumbra area.

Usage:
    python manage.py seed_data            # adds records, skips if already present
    python manage.py seed_data --flush    # clears existing data first
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from healthcare.models import BedStatus, Doctor, HealthcareFacility, Pharmacy


FACILITIES = [
    # ── Kausa ────────────────────────────────────────────────────────────────
    {
        'name': 'Kausa Municipal Hospital',
        'facility_type': 'HOSPITAL',
        'area': 'KAUSA',
        'address': 'Kausa Village Road, Mumbra, Thane - 400612',
        'contact_number': '02225340001',
        'whatsapp_number': '919822000001',
        'is_verified': True,
        'beds': {'total_beds': 80, 'available_beds': 24, 'icu_total': 10, 'icu_available': 3},
        'doctors': [
            {'name': 'Arshad Khan', 'specialty': 'GENERAL', 'contact_number': '919800000001',
             'timing_slots': {'Mon-Sat': '9:00–13:00', 'Eve': '17:00–20:00'}},
            {'name': 'Sunita Patil', 'specialty': 'GYNAE', 'contact_number': '919800000002',
             'timing_slots': {'Mon-Fri': '10:00–14:00'}},
        ],
    },
    {
        'name': 'Al-Shifa Clinic',
        'facility_type': 'CLINIC',
        'area': 'KAUSA',
        'address': 'Shop 4, Kausa Naka, Mumbra - 400612',
        'contact_number': '02225340002',
        'whatsapp_number': '919822000002',
        'is_verified': True,
        'beds': {'total_beds': 10, 'available_beds': 4, 'icu_total': 0, 'icu_available': 0},
        'doctors': [
            {'name': 'Mohammed Raza', 'specialty': 'PEDIATRIC', 'contact_number': '919800000003',
             'timing_slots': {'Mon-Sun': '8:00–12:00', 'Eve': '16:00–21:00'}},
        ],
    },
    {
        'name': 'Noor Heart & Care Clinic',
        'facility_type': 'CLINIC',
        'area': 'KAUSA',
        'address': 'Near Kausa Police Station, Mumbra',
        'contact_number': '02225340003',
        'whatsapp_number': '',
        'is_verified': False,
        'beds': {'total_beds': 5, 'available_beds': 2, 'icu_total': 0, 'icu_available': 0},
        'doctors': [
            {'name': 'Farhan Siddiqui', 'specialty': 'CARDIAC', 'contact_number': '919800000004',
             'timing_slots': {'Mon-Sat': '11:00–15:00'}},
        ],
    },

    # ── Amrut Nagar ──────────────────────────────────────────────────────────
    {
        'name': 'Mumbra General Hospital',
        'facility_type': 'HOSPITAL',
        'area': 'AMRUT_NAGAR',
        'address': 'Amrut Nagar, Mumbra, Thane - 400612',
        'contact_number': '02225341000',
        'whatsapp_number': '919822001000',
        'is_verified': True,
        'beds': {'total_beds': 120, 'available_beds': 8, 'icu_total': 20, 'icu_available': 2},
        'doctors': [
            {'name': 'Priya Sharma', 'specialty': 'GENERAL', 'contact_number': '919800001001',
             'timing_slots': {'Mon-Sat': '9:00–13:00', 'Eve': '18:00–21:00'}},
            {'name': 'Dr. Ahmed Ansari', 'specialty': 'ORTHO', 'contact_number': '919800001002',
             'timing_slots': {'Mon-Fri': '10:00–14:00'}},
            {'name': 'Kavita Desai', 'specialty': 'PEDIATRIC', 'contact_number': '919800001003',
             'timing_slots': {'Mon-Sun': '8:00–12:00'}},
        ],
    },
    {
        'name': 'Amrut Nagar Polyclinic',
        'facility_type': 'CLINIC',
        'area': 'AMRUT_NAGAR',
        'address': 'Plot 12, Amrut Nagar Main Road, Mumbra',
        'contact_number': '02225341001',
        'whatsapp_number': '',
        'is_verified': True,
        'beds': {'total_beds': 15, 'available_beds': 0, 'icu_total': 0, 'icu_available': 0},
        'doctors': [
            {'name': 'Ruksana Shaikh', 'specialty': 'DERM', 'contact_number': '919800001004',
             'timing_slots': {'Mon-Sun': '10:00–14:00', 'Eve': '17:00–20:00'}},
        ],
    },
    {
        'name': 'Crescent ENT & Eye Hospital',
        'facility_type': 'HOSPITAL',
        'area': 'AMRUT_NAGAR',
        'address': 'Crescent Road, Amrut Nagar, Mumbra',
        'contact_number': '02225341002',
        'whatsapp_number': '919822001002',
        'is_verified': True,
        'beds': {'total_beds': 30, 'available_beds': 12, 'icu_total': 4, 'icu_available': 1},
        'doctors': [
            {'name': 'Imran Sheikh', 'specialty': 'ENT', 'contact_number': '919800001005',
             'timing_slots': {'Mon-Sat': '9:00–13:00', 'Eve': '18:00–21:00'}},
        ],
    },

    # ── Station Road ─────────────────────────────────────────────────────────
    {
        'name': 'Mumbra Station Road Hospital',
        'facility_type': 'HOSPITAL',
        'area': 'STATION_ROAD',
        'address': 'Station Road, Mumbra, Thane - 400612',
        'contact_number': '02225342000',
        'whatsapp_number': '919822002000',
        'is_verified': True,
        'beds': {'total_beds': 60, 'available_beds': 18, 'icu_total': 8, 'icu_available': 4},
        'doctors': [
            {'name': 'Salim Mansuri', 'specialty': 'GENERAL', 'contact_number': '919800002001',
             'timing_slots': {'Mon-Sat': '8:00–12:00', 'Eve': '17:00–21:00'}},
            {'name': 'Neha Kulkarni', 'specialty': 'GYNAE', 'contact_number': '919800002002',
             'timing_slots': {'Mon-Fri': '10:00–14:00'}},
            {'name': 'Anwar Ali', 'specialty': 'CARDIAC', 'contact_number': '919800002003',
             'timing_slots': {'Mon-Sat': '11:00–15:00', 'Eve': '19:00–21:00'}},
        ],
    },
    {
        'name': 'Shifa Maternity & Child Clinic',
        'facility_type': 'CLINIC',
        'area': 'STATION_ROAD',
        'address': 'Near Mumbra Station, Station Road, Mumbra',
        'contact_number': '02225342001',
        'whatsapp_number': '919822002001',
        'is_verified': True,
        'beds': {'total_beds': 20, 'available_beds': 6, 'icu_total': 0, 'icu_available': 0},
        'doctors': [
            {'name': 'Dr. Zubeda Khan', 'specialty': 'PEDIATRIC', 'contact_number': '919800002004',
             'timing_slots': {'Mon-Sun': '9:00–21:00'}},
        ],
    },
]


PHARMACIES = [
    # Kausa
    {'name': 'Al-Madina Medical', 'area': 'KAUSA',
     'address': 'Kausa Naka, Mumbra', 'contact_number': '02225340100',
     'is_24_7': True, 'is_verified': True},
    {'name': 'New Life Pharma', 'area': 'KAUSA',
     'address': 'Station Road Junction, Kausa', 'contact_number': '02225340101',
     'is_24_7': False, 'opening_time': '08:00', 'closing_time': '23:00', 'is_verified': True},
    {'name': 'Kausa Medical Store', 'area': 'KAUSA',
     'address': 'Opposite Kausa Hospital', 'contact_number': '02225340102',
     'is_24_7': False, 'opening_time': '09:00', 'closing_time': '22:00', 'is_verified': False},

    # Amrut Nagar
    {'name': 'Crescent Pharmacy', 'area': 'AMRUT_NAGAR',
     'address': 'Amrut Nagar Main Road', 'contact_number': '02225341100',
     'is_24_7': True, 'is_verified': True},
    {'name': 'Rahmat Medical', 'area': 'AMRUT_NAGAR',
     'address': 'Shop 7, Amrut Nagar Market', 'contact_number': '02225341101',
     'is_24_7': False, 'opening_time': '08:30', 'closing_time': '23:30', 'is_verified': True},

    # Station Road
    {'name': 'Station Road Medicals', 'area': 'STATION_ROAD',
     'address': 'Opp. Mumbra Railway Station', 'contact_number': '02225342100',
     'is_24_7': True, 'is_verified': True},
    {'name': 'Apollo Pharmacy Mumbra', 'area': 'STATION_ROAD',
     'address': 'Ground Floor, Station Plaza, Mumbra', 'contact_number': '02225342101',
     'is_24_7': True, 'is_verified': True},
    {'name': 'Bismillah Medical Store', 'area': 'STATION_ROAD',
     'address': 'Near Mumbra Police Station', 'contact_number': '02225342102',
     'is_24_7': False, 'opening_time': '07:00', 'closing_time': '00:00', 'is_verified': False},
]


class Command(BaseCommand):
    help = 'Seed the database with representative Mumbra healthcare data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Delete all existing data before seeding',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options['flush']:
            self.stdout.write('  Flushing existing data…')
            BedStatus.objects.all().delete()
            Doctor.objects.all().delete()
            HealthcareFacility.objects.all().delete()
            Pharmacy.objects.all().delete()
            self.stdout.write(self.style.WARNING('  Data cleared.'))

        self.stdout.write(self.style.MIGRATE_HEADING('\nSeeding healthcare facilities…'))
        facility_count = doctor_count = 0

        for fdata in FACILITIES:
            bed_data = fdata.pop('beds')
            doctor_data = fdata.pop('doctors')

            facility, created = HealthcareFacility.objects.get_or_create(
                name=fdata['name'],
                area=fdata['area'],
                defaults=fdata,
            )
            if created:
                facility_count += 1
                self.stdout.write(f'  ✓ {facility}')
            else:
                self.stdout.write(f'  ~ {facility} (already exists)')

            # Bed status
            BedStatus.objects.update_or_create(
                facility=facility,
                defaults=bed_data,
            )

            # Doctors
            for ddata in doctor_data:
                timing = ddata.pop('timing_slots', {})
                doc, dcreated = Doctor.objects.get_or_create(
                    name=ddata['name'],
                    facility=facility,
                    defaults={**ddata, 'timing_slots': timing},
                )
                if dcreated:
                    doctor_count += 1

        self.stdout.write(self.style.MIGRATE_HEADING('\nSeeding pharmacies…'))
        pharmacy_count = 0

        for pdata in PHARMACIES:
            # Convert time strings to time objects if provided
            for tf in ('opening_time', 'closing_time'):
                raw = pdata.get(tf)
                if raw:
                    from datetime import time as dtime
                    h, m = map(int, raw.split(':'))
                    pdata[tf] = dtime(h, m)

            _, created = Pharmacy.objects.get_or_create(
                name=pdata['name'],
                area=pdata['area'],
                defaults=pdata,
            )
            if created:
                pharmacy_count += 1
                self.stdout.write(f'  ✓ {pdata["name"]}')
            else:
                self.stdout.write(f'  ~ {pdata["name"]} (already exists)')

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Seeding complete — '
                f'{facility_count} facilities, {doctor_count} doctors, {pharmacy_count} pharmacies added.'
            )
        )
