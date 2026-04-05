from django.contrib import admin
from django.utils.html import format_html

from .models import Advertisement, BedStatus, Doctor, HealthcareFacility, Pharmacy, SiteSettings


class BedStatusInline(admin.StackedInline):
    model = BedStatus
    extra = 0
    fields = ('total_beds', 'available_beds', 'icu_total', 'icu_available', 'updated_by')


class DoctorInline(admin.TabularInline):
    model = Doctor
    extra = 0
    fields = ('name', 'specialty', 'contact_number', 'is_available')
    show_change_link = True


@admin.register(HealthcareFacility)
class HealthcareFacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'facility_type', 'area', 'contact_number', 'is_verified', 'is_active')
    list_filter = ('facility_type', 'area', 'is_verified', 'is_active')
    search_fields = ('name', 'address')
    list_editable = ('is_verified', 'is_active')
    inlines = [BedStatusInline, DoctorInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'facility_type', 'area', 'user', 'is_verified', 'is_active'),
        }),
        ('Contact', {
            'fields': ('address', 'contact_number', 'whatsapp_number'),
        }),
    )


@admin.register(BedStatus)
class BedStatusAdmin(admin.ModelAdmin):
    list_display = ('facility', 'available_beds', 'total_beds', 'icu_available', 'icu_total', 'last_updated')
    list_filter = ('facility__area',)
    search_fields = ('facility__name',)
    readonly_fields = ('last_updated',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'facility', 'is_available', 'last_status_update')
    list_filter = ('specialty', 'is_available', 'facility__area')
    search_fields = ('name', 'facility__name')
    list_editable = ('is_available',)
    readonly_fields = ('last_status_update',)
    fieldsets = (
        (None, {
            'fields': ('name', 'specialty', 'facility', 'user', 'contact_number', 'is_available'),
        }),
        ('Schedule', {
            'fields': ('timing_slots', 'last_status_update'),
        }),
    )


@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ('name', 'area', 'is_24_7', 'contact_number', 'is_verified', 'is_active')
    list_filter = ('area', 'is_24_7', 'is_verified', 'is_active')
    search_fields = ('name', 'address')
    list_editable = ('is_24_7', 'is_verified', 'is_active')
    fieldsets = (
        (None, {
            'fields': ('name', 'area', 'user', 'is_24_7', 'is_verified', 'is_active'),
        }),
        ('Contact', {
            'fields': ('address', 'contact_number', 'opening_time', 'closing_time'),
        }),
    )


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('short_text', 'preview_image', 'order', 'is_active', 'created_at')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    ordering = ('order', 'created_at')

    @admin.display(description='Ad Text')
    def short_text(self, obj):
        return obj.text[:60]

    @admin.display(description='Image Preview')
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:36px;border-radius:4px;" />', obj.image.url)
        return '—'


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Singleton — always shows only one row; Save replaces it."""
    list_display = ('donate_name', 'donate_upi_id', 'qr_preview')
    fields = ('donate_name', 'donate_upi_id', 'paytm_qr_image', 'qr_preview')
    readonly_fields = ('qr_preview',)

    @admin.display(description='QR Preview')
    def qr_preview(self, obj):
        if obj.paytm_qr_image:
            return format_html('<img src="{}" style="height:120px;border-radius:8px;" />', obj.paytm_qr_image.url)
        return 'No QR uploaded yet.'

    def has_add_permission(self, request):
        # Allow add only if no row exists
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False  # Prevent accidental deletion

