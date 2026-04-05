from django.contrib.auth.models import User
from rest_framework import serializers
from .models import BedStatus, Doctor, HealthcareFacility, Pharmacy


class BedStatusSerializer(serializers.ModelSerializer):
    is_available = serializers.BooleanField(read_only=True)

    class Meta:
        model = BedStatus
        fields = [
            'total_beds',
            'available_beds',
            'icu_total',
            'icu_available',
            'is_available',
            'last_updated',
        ]


class HealthcareFacilitySerializer(serializers.ModelSerializer):
    bed_status = BedStatusSerializer(read_only=True)
    area_display = serializers.CharField(source='get_area_display', read_only=True)
    facility_type_display = serializers.CharField(source='get_facility_type_display', read_only=True)

    class Meta:
        model = HealthcareFacility
        fields = [
            'id',
            'name',
            'facility_type',
            'facility_type_display',
            'area',
            'area_display',
            'address',
            'contact_number',
            'whatsapp_number',
            'is_verified',
            'bed_status',
        ]


class DoctorSerializer(serializers.ModelSerializer):
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    facility_area = serializers.CharField(source='facility.get_area_display', read_only=True)
    facility_address = serializers.CharField(source='facility.address', read_only=True)
    specialty_display = serializers.CharField(source='get_specialty_display', read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id',
            'name',
            'specialty',
            'specialty_display',
            'facility',
            'facility_name',
            'facility_area',
            'facility_address',
            'contact_number',
            'is_available',
            'timing_slots',
            'last_status_update',
        ]


class DoctorStatusUpdateSerializer(serializers.ModelSerializer):
    """Lightweight serializer for toggling doctor availability."""

    class Meta:
        model = Doctor
        fields = ['is_available']


class PharmacySerializer(serializers.ModelSerializer):
    area_display = serializers.CharField(source='get_area_display', read_only=True)

    class Meta:
        model = Pharmacy
        fields = [
            'id',
            'name',
            'area',
            'area_display',
            'address',
            'contact_number',
            'is_24_7',
            'opening_time',
            'closing_time',
            'is_verified',
        ]


# ─── Portal serializers ──────────────────────────────────────────────────────

class PortalFacilitySerializer(serializers.ModelSerializer):
    """Facility portal: view + update own facility info."""
    area_display = serializers.CharField(source='get_area_display', read_only=True)
    bed_status = BedStatusSerializer(read_only=True)

    class Meta:
        model = HealthcareFacility
        fields = [
            'id', 'name', 'facility_type', 'area', 'area_display',
            'address', 'contact_number', 'whatsapp_number',
            'is_verified', 'bed_status',
        ]
        read_only_fields = ['id', 'area_display', 'is_verified', 'bed_status']


class PortalBedUpdateSerializer(serializers.ModelSerializer):
    """Facility portal: update bed counts with validation."""

    class Meta:
        model = BedStatus
        fields = ['total_beds', 'available_beds', 'icu_total', 'icu_available', 'last_updated']
        read_only_fields = ['last_updated']

    def validate(self, data):
        inst = self.instance
        total = data.get('total_beds', inst.total_beds if inst else 0)
        available = data.get('available_beds', inst.available_beds if inst else 0)
        icu_total = data.get('icu_total', inst.icu_total if inst else 0)
        icu_available = data.get('icu_available', inst.icu_available if inst else 0)
        if available > total:
            raise serializers.ValidationError({'available_beds': 'Cannot exceed total beds.'})
        if icu_available > icu_total:
            raise serializers.ValidationError({'icu_available': 'Cannot exceed ICU total.'})
        return data


class PortalDoctorSerializer(serializers.ModelSerializer):
    """Doctor portal: view + update own profile."""
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    facility_address = serializers.CharField(source='facility.address', read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id', 'name', 'specialty', 'facility', 'facility_name',
            'facility_address', 'contact_number', 'is_available',
            'timing_slots', 'last_status_update',
        ]
        read_only_fields = ['id', 'facility', 'facility_name', 'facility_address', 'last_status_update']


class PortalPharmacySerializer(serializers.ModelSerializer):
    """Pharmacy portal: view + update own pharmacy profile."""
    area_display = serializers.CharField(source='get_area_display', read_only=True)

    class Meta:
        model = Pharmacy
        fields = [
            'id', 'name', 'area', 'area_display', 'address', 'contact_number',
            'is_24_7', 'opening_time', 'closing_time', 'is_verified',
        ]
        read_only_fields = ['id', 'area', 'area_display', 'is_verified']


class PortalUserSerializer(serializers.ModelSerializer):
    """Admin portal: view and lightly edit any portal user."""
    user_type = serializers.SerializerMethodField()
    profile_name = serializers.SerializerMethodField()
    profile_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'is_active', 'is_staff',
            'user_type', 'profile_id', 'profile_name', 'date_joined',
        ]
        read_only_fields = ['id', 'user_type', 'profile_name', 'date_joined']

    def get_user_type(self, obj):
        if obj.is_staff:
            return 'ADMIN'
        if hasattr(obj, 'facility_profile'):
            return 'FACILITY'
        if hasattr(obj, 'doctor_profile'):
            return 'DOCTOR'
        if hasattr(obj, 'pharmacy_profile'):
            return 'PHARMACY'
        return 'STAFF'

    def get_profile_name(self, obj):
        if hasattr(obj, 'facility_profile'):
            return obj.facility_profile.name
        if hasattr(obj, 'doctor_profile'):
            return f"Dr. {obj.doctor_profile.name}"
        if hasattr(obj, 'pharmacy_profile'):
            return obj.pharmacy_profile.name
        return ''

    def get_profile_id(self, obj):
        if hasattr(obj, 'facility_profile'):
            return obj.facility_profile.id
        if hasattr(obj, 'doctor_profile'):
            return obj.doctor_profile.id
        if hasattr(obj, 'pharmacy_profile'):
            return obj.pharmacy_profile.id
        return None


class PortalUserCreateSerializer(serializers.Serializer):
    """Admin portal: create a portal user and link to a facility or doctor."""
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    is_staff = serializers.BooleanField(default=False)
    link_to_facility = serializers.IntegerField(required=False, allow_null=True)
    link_to_doctor = serializers.IntegerField(required=False, allow_null=True)
    link_to_pharmacy = serializers.IntegerField(required=False, allow_null=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already taken.')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already registered.')
        return value

    def validate(self, data):
        facility_id = data.get('link_to_facility')
        doctor_id = data.get('link_to_doctor')
        pharmacy_id = data.get('link_to_pharmacy')
        links = [value for value in (facility_id, doctor_id, pharmacy_id) if value]
        if len(links) > 1:
            raise serializers.ValidationError('Cannot link a user to more than one profile type.')
        if not data.get('is_staff') and len(links) == 0:
            raise serializers.ValidationError(
                'Non-admin portal users must be linked to a facility, doctor, or pharmacy.'
            )
        if facility_id:
            try:
                facility = HealthcareFacility.objects.get(pk=facility_id)
                if facility.user_id:
                    raise serializers.ValidationError(
                        {'link_to_facility': 'This facility already has a portal user.'})
                data['_facility'] = facility
            except HealthcareFacility.DoesNotExist:
                raise serializers.ValidationError({'link_to_facility': 'Facility not found.'})
        if doctor_id:
            try:
                doctor = Doctor.objects.get(pk=doctor_id)
                if doctor.user_id:
                    raise serializers.ValidationError(
                        {'link_to_doctor': 'This doctor already has a portal user.'})
                data['_doctor'] = doctor
            except Doctor.DoesNotExist:
                raise serializers.ValidationError({'link_to_doctor': 'Doctor not found.'})
        if pharmacy_id:
            try:
                pharmacy = Pharmacy.objects.get(pk=pharmacy_id)
                if pharmacy.user_id:
                    raise serializers.ValidationError(
                        {'link_to_pharmacy': 'This pharmacy already has a portal user.'})
                data['_pharmacy'] = pharmacy
            except Pharmacy.DoesNotExist:
                raise serializers.ValidationError({'link_to_pharmacy': 'Pharmacy not found.'})
        return data

    def create(self, validated_data):
        facility = validated_data.pop('_facility', None)
        doctor = validated_data.pop('_doctor', None)
        pharmacy = validated_data.pop('_pharmacy', None)
        validated_data.pop('link_to_facility', None)
        validated_data.pop('link_to_doctor', None)
        validated_data.pop('link_to_pharmacy', None)
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        if facility:
            facility.user = user
            facility.save(update_fields=['user'])
        if doctor:
            doctor.user = user
            doctor.save(update_fields=['user'])
        if pharmacy:
            pharmacy.user = user
            pharmacy.save(update_fields=['user'])
        return user
