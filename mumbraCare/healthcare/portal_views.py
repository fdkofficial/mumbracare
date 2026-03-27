"""
Portal views — facility owners, doctors, and admins manage their own data.

Auth:  Bearer JWT token (from /api/auth/login/)
Roles: FACILITY  → linked via HealthcareFacility.user
       DOCTOR    → linked via Doctor.user
       ADMIN     → user.is_staff = True
"""
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BedStatus, Doctor, HealthcareFacility
from .permissions import IsDoctorOwner, IsFacilityOwner, IsPortalAdmin
from .serializers import (
    PortalBedUpdateSerializer,
    PortalDoctorSerializer,
    PortalFacilitySerializer,
    PortalUserCreateSerializer,
    PortalUserSerializer,
)


def _user_type(user):
    if user.is_staff:
        return 'ADMIN'
    if hasattr(user, 'facility_profile'):
        return 'FACILITY'
    if hasattr(user, 'doctor_profile'):
        return 'DOCTOR'
    return 'UNKNOWN'


# ─── Auth / Me ───────────────────────────────────────────────────────────────

class MeView(APIView):
    """GET /api/auth/me/ — return current user info and their portal role."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        utype = _user_type(user)
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
            'user_type': utype,
            'profile_id': None,
            'profile_name': '',
        }
        if utype == 'FACILITY':
            data['profile_id'] = user.facility_profile.id
            data['profile_name'] = user.facility_profile.name
        elif utype == 'DOCTOR':
            data['profile_id'] = user.doctor_profile.id
            data['profile_name'] = f"Dr. {user.doctor_profile.name}"
        return Response(data)


# ─── Facility portal ─────────────────────────────────────────────────────────

class FacilityPortalView(APIView):
    """GET/PATCH /api/portal/facility/ — facility owner manages their facility."""
    permission_classes = [IsAuthenticated, IsFacilityOwner]

    def get(self, request):
        serializer = PortalFacilitySerializer(request.user.facility_profile)
        return Response(serializer.data)

    def patch(self, request):
        serializer = PortalFacilitySerializer(
            request.user.facility_profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class FacilityBedsPortalView(APIView):
    """GET/PATCH /api/portal/facility/beds/ — facility owner updates bed counts."""
    permission_classes = [IsAuthenticated, IsFacilityOwner]

    def _get_or_create(self, request):
        return BedStatus.objects.get_or_create(facility=request.user.facility_profile)

    def get(self, request):
        bed_status, _ = self._get_or_create(request)
        return Response(PortalBedUpdateSerializer(bed_status).data)

    def patch(self, request):
        bed_status, _ = self._get_or_create(request)
        serializer = PortalBedUpdateSerializer(bed_status, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        return Response(serializer.data)


# ─── Doctor portal ───────────────────────────────────────────────────────────

class DoctorPortalView(APIView):
    """GET/PATCH /api/portal/doctor/ — doctor manages their own profile."""
    permission_classes = [IsAuthenticated, IsDoctorOwner]

    def get(self, request):
        return Response(PortalDoctorSerializer(request.user.doctor_profile).data)

    def patch(self, request):
        serializer = PortalDoctorSerializer(
            request.user.doctor_profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class DoctorStatusPortalView(APIView):
    """PATCH /api/portal/doctor/status/ — doctor toggles in-clinic status."""
    permission_classes = [IsAuthenticated, IsDoctorOwner]

    def patch(self, request):
        doctor = request.user.doctor_profile
        is_available = request.data.get('is_available')
        doctor.is_available = bool(is_available) if is_available is not None else not doctor.is_available
        doctor.save(update_fields=['is_available', 'last_status_update'])
        return Response({'is_available': doctor.is_available})


# ─── Admin portal (user management) ─────────────────────────────────────────

class AdminUserListView(APIView):
    """GET/POST /api/portal/admin/users/ — admin lists or creates portal users."""
    permission_classes = [IsAuthenticated, IsPortalAdmin]

    def get(self, request):
        # Exclude superusers from list (they're managed via Django admin only)
        users = (
            User.objects
            .filter(is_superuser=False)
            .select_related('facility_profile', 'doctor_profile')
            .order_by('username')
        )
        return Response(PortalUserSerializer(users, many=True).data)

    def post(self, request):
        serializer = PortalUserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(PortalUserSerializer(user).data, status=status.HTTP_201_CREATED)


class AdminUserDetailView(APIView):
    """GET/PATCH/DELETE /api/portal/admin/users/<pk>/ — admin manages a portal user."""
    permission_classes = [IsAuthenticated, IsPortalAdmin]

    def _get_user(self, pk):
        try:
            return User.objects.select_related(
                'facility_profile', 'doctor_profile').get(pk=pk, is_superuser=False)
        except User.DoesNotExist:
            return None

    def get(self, request, pk):
        user = self._get_user(pk)
        if not user:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(PortalUserSerializer(user).data)

    def patch(self, request, pk):
        user = self._get_user(pk)
        if not user:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        # Allow updating email, is_active, is_staff; block username changes via PATCH
        allowed = {k: v for k, v in request.data.items() if k in ('email', 'is_active', 'is_staff')}
        # Handle password reset separately (secure)
        new_password = request.data.get('password')
        if new_password:
            if len(new_password) < 8:
                return Response(
                    {'password': 'Password must be at least 8 characters.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.set_password(new_password)
        serializer = PortalUserSerializer(user, data=allowed, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if new_password:
            user.save()
        return Response(PortalUserSerializer(user).data)

    def delete(self, request, pk):
        user = self._get_user(pk)
        if not user:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        # Soft-delete: deactivate rather than hard delete
        user.is_active = False
        user.save(update_fields=['is_active'])
        return Response({'detail': f'User {user.username} deactivated.'})
