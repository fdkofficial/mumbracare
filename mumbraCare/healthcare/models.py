from django.db import models
from django.contrib.auth.models import User


class HealthcareFacility(models.Model):
    FACILITY_TYPES = [
        ('HOSPITAL', 'Hospital'),
        ('CLINIC', 'Clinic'),
    ]
    AREA_CHOICES = [
        ('KAUSA', 'Kausa'),
        ('AMRUT_NAGAR', 'Amrut Nagar'),
        ('STATION_ROAD', 'Station Road'),
    ]

    name = models.CharField(max_length=255)
    facility_type = models.CharField(choices=FACILITY_TYPES, max_length=20)
    area = models.CharField(choices=AREA_CHOICES, max_length=50)
    address = models.TextField()
    contact_number = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='facility_profile',
        help_text='Portal login user for this facility',
    )

    class Meta:
        verbose_name_plural = 'Healthcare Facilities'
        ordering = ['area', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_area_display()})"


class BedStatus(models.Model):
    facility = models.OneToOneField(
        HealthcareFacility,
        on_delete=models.CASCADE,
        related_name='bed_status',
    )
    total_beds = models.PositiveIntegerField(default=0)
    available_beds = models.PositiveIntegerField(default=0)
    icu_total = models.PositiveIntegerField(default=0)
    icu_available = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        'auth.User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='bed_updates',
    )

    class Meta:
        verbose_name = 'Bed Status'
        verbose_name_plural = 'Bed Statuses'

    def __str__(self):
        return f"{self.facility.name} — {self.available_beds}/{self.total_beds} beds"

    @property
    def is_available(self):
        return self.available_beds > 0


class Doctor(models.Model):
    SPECIALTIES = [
        ('PEDIATRIC', 'Pediatrician'),
        ('CARDIAC', 'Cardiac Expert'),
        ('GENERAL', 'General Physician'),
        ('GYNAE', 'Gynaecologist'),
        ('ORTHO', 'Orthopaedic'),
        ('DERM', 'Dermatologist'),
        ('ENT', 'ENT Specialist'),
    ]

    name = models.CharField(max_length=255)
    specialty = models.CharField(choices=SPECIALTIES, max_length=50)
    facility = models.ForeignKey(
        HealthcareFacility,
        on_delete=models.CASCADE,
        related_name='doctors',
    )
    contact_number = models.CharField(max_length=20, blank=True)
    is_available = models.BooleanField(default=True)
    timing_slots = models.JSONField(
        default=dict,
        help_text='e.g. {"mon-sat": "10:00-13:00", "eve": "18:00-21:00"}',
    )
    last_status_update = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='doctor_profile',
        help_text='Portal login user for this doctor',
    )

    class Meta:
        ordering = ['specialty', 'name']

    def __str__(self):
        status = 'IN' if self.is_available else 'OUT'
        return f"Dr. {self.name} [{self.get_specialty_display()}] — {status}"


class Pharmacy(models.Model):
    AREA_CHOICES = HealthcareFacility.AREA_CHOICES

    name = models.CharField(max_length=255)
    area = models.CharField(choices=AREA_CHOICES, max_length=50)
    address = models.TextField()
    contact_number = models.CharField(max_length=20)
    is_24_7 = models.BooleanField(default=False)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Pharmacies'
        ordering = ['area', 'name']

    def __str__(self):
        tag = '24/7' if self.is_24_7 else f"{self.opening_time}–{self.closing_time}"
        return f"{self.name} ({self.get_area_display()}) [{tag}]"


class Advertisement(models.Model):
    """Rotating banner ads shown at the bottom of the public app."""

    text = models.CharField(max_length=150, help_text='Short ad text displayed in the banner.')
    image = models.ImageField(
        upload_to='ads/',
        blank=True,
        null=True,
        help_text='Optional banner image. If set, shown instead of text.',
    )
    link_url = models.URLField(blank=True, help_text='Optional tap-through URL.')
    is_active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0, help_text='Lower number = shown first.')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Advertisement'

    def __str__(self):
        return self.text[:60]


class SiteSettings(models.Model):
    """Singleton model — only one row should exist. Stores global site config."""

    paytm_qr_image = models.ImageField(
        upload_to='donate/',
        blank=True,
        null=True,
        help_text='Paytm / UPI QR code image shown in the "Thank You" donate popup.',
    )
    donate_name = models.CharField(
        max_length=100,
        default='Mumbra Care',
        help_text='Name shown below the QR code.',
    )
    donate_upi_id = models.CharField(
        max_length=100,
        blank=True,
        help_text='UPI ID shown below the QR code (e.g. mumbracare@paytm).',
    )

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return 'Site Settings'

    def save(self, *args, **kwargs):
        # Enforce singleton: delete any other row
        self.__class__.objects.exclude(pk=self.pk).delete()
        super().save(*args, **kwargs)
