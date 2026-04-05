"""
Management command: seed_data

Seeds the database with publicly discoverable Mumbra healthcare data.

Facility names, addresses, and contacts below were curated from official sites
or public business directories. Bed availability and some operational fields are
kept conservative when a live value was not publicly available.

Usage:
    python manage.py seed_data            # adds records, skips if already present
    python manage.py seed_data --flush    # clears existing data first
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from healthcare.models import BedStatus, Doctor, HealthcareFacility, Pharmacy


FACILITIES = [
    {
        'name': 'Freedom Fighter Hakim Ajmal Khan TMC Hospital',
        'facility_type': 'HOSPITAL',
        'area': 'KAUSA',
        'address': 'MM Valley Road, Kausa, Mumbra, Thane, Maharashtra 400612',
        'contact_number': '9987229960',
        'whatsapp_number': '9987229960',
        'is_verified': True,
        'beds': {'total_beds': 100, 'available_beds': 0, 'icu_total': 0, 'icu_available': 0},
        'doctors': [],
    },
    {
        'name': 'GHC Hospitals',
        'facility_type': 'HOSPITAL',
        'area': 'KAUSA',
        'address': 'Thane Shil Road, Kausa, Thane, Maharashtra 400612',
        'contact_number': '02231007444',
        'whatsapp_number': '918104242551',
        'is_verified': True,
        'beds': {'total_beds': 140, 'available_beds': 0, 'icu_total': 24, 'icu_available': 0},
        'doctors': [
            {'name': 'Dr. Ram Shinde', 'specialty': 'GENERAL', 'contact_number': '', 'timing_slots': {}},
            {'name': 'Dr. Neerja Gupta', 'specialty': 'GYNAE', 'contact_number': '', 'timing_slots': {}},
            {'name': 'Dr. Talib Surve', 'specialty': 'PEDIATRIC', 'contact_number': '', 'timing_slots': {}},
            {'name': 'Dr. Suheil Dhanse', 'specialty': 'CARDIAC', 'contact_number': '', 'timing_slots': {}},
            {'name': 'Dr. Faisal Husain Bape', 'specialty': 'ORTHO', 'contact_number': '', 'timing_slots': {}},
            {'name': 'Dr. Safa Imtyaz Patrick', 'specialty': 'DERM', 'contact_number': '', 'timing_slots': {}},
            {'name': 'Dr. Pravin Rajgadkar', 'specialty': 'ENT', 'contact_number': '', 'timing_slots': {}},
        ],
    },
    {
        'name': 'Burhani Hospital',
        'facility_type': 'HOSPITAL',
        'area': 'STATION_ROAD',
        'address': 'Police Station, Dr Syedna Mohammed Burhanuddin Marg, near Mumbra, Zainy Colony, Mumbra, Thane, Maharashtra 400612',
        'contact_number': '02225460115',
        'whatsapp_number': '',
        'is_verified': True,
        'beds': {'total_beds': 20, 'available_beds': 0, 'icu_total': 3, 'icu_available': 0},
        'doctors': [
            {'name': 'Dr. Firdousara Siddiqui', 'specialty': 'GYNAE', 'contact_number': '',
             'timing_slots': {'Mon-Sat': '12:00-14:00', 'Eve': '17:00-19:00'}},
        ],
    },
]


PHARMACIES = [
    {
        'name': 'Zeelab Pharmacy Medical Store',
        'area': 'KAUSA',
        'address': 'Pleasure Garden, Kausa Village, Mumbra, Thane, Maharashtra 400612',
        'contact_number': '9987876714',
        'is_24_7': False,
        'opening_time': '09:00',
        'closing_time': '21:00',
        'is_verified': True,
    },
    {
        'name': 'Apollo Pharmacy Mumbra',
        'area': 'STATION_ROAD',
        'address': 'Shop No.4, Ground Floor, Marina Building, Opp Mumbra Station, Mumbra, Thane, 400612',
        'contact_number': '9372676466',
        'is_24_7': False,
        'opening_time': '07:00',
        'closing_time': '23:00',
        'is_verified': True,
    },
]


class Command(BaseCommand):
    help = 'Seed the database with curated public Mumbra healthcare data'

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

        for seed_facility in FACILITIES:
            fdata = {k: v for k, v in seed_facility.items() if k not in ('beds', 'doctors')}
            bed_data = dict(seed_facility['beds'])
            doctor_data = [dict(doctor) for doctor in seed_facility['doctors']]

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

        for seed_pharmacy in PHARMACIES:
            pdata = dict(seed_pharmacy)
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
