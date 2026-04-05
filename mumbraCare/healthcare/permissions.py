from rest_framework.permissions import BasePermission


class IsFacilityOwner(BasePermission):
    """Allow access only to the portal user linked to a healthcare facility."""

    message = 'Your account is not linked to any healthcare facility.'

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'facility_profile')
        )


class IsDoctorOwner(BasePermission):
    """Allow access only to the portal user linked to a doctor profile."""

    message = 'Your account is not linked to any doctor profile.'

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'doctor_profile')
        )


class IsPharmacyOwner(BasePermission):
    """Allow access only to the portal user linked to a pharmacy profile."""

    message = 'Your account is not linked to any pharmacy profile.'

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'pharmacy_profile')
        )


class IsPortalAdmin(BasePermission):
    """Allow access only to staff (admin) users."""

    message = 'Admin access required.'

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )
