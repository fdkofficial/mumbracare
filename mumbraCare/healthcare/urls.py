from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .portal_views import (
    MeView,
    FacilityPortalView, FacilityBedsPortalView,
    DoctorPortalView, DoctorStatusPortalView,
    AdminUserListView, AdminUserDetailView,
)
from .whatsapp_views import WhatsAppWebhookView

urlpatterns = [
    # Liveness / health check
    path('health/', views.health_check, name='health-check'),

    # Public content
    path('ads/', views.PublicAdsView.as_view(), name='ads'),
    path('site-settings/', views.PublicSettingsView.as_view(), name='site-settings'),

    # Facilities
    path('facilities/', views.FacilityListView.as_view(), name='facility-list'),
    path('facilities/<int:pk>/', views.FacilityDetailView.as_view(), name='facility-detail'),

    # Bed tracker — the "Green Means Ready" dashboard
    path('beds/', views.BedTrackerView.as_view(), name='bed-tracker'),

    # Doctor directory & status toggle
    path('doctors/', views.DoctorListView.as_view(), name='doctor-list'),
    path('doctors/<int:pk>/status/', views.DoctorStatusUpdateView.as_view(), name='doctor-status'),

    # Night pharmacy directory
    path('pharmacies/', views.PharmacyListView.as_view(), name='pharmacy-list'),

    # WhatsApp webhook (Twilio posts here)
    path('whatsapp/webhook/', WhatsAppWebhookView.as_view(), name='whatsapp-webhook'),

    # ─── Auth ────────────────────────────────────────────────────────────────
    path('auth/login/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('auth/me/', MeView.as_view(), name='auth-me'),

    # ─── Facility portal ─────────────────────────────────────────────────────
    path('portal/facility/', FacilityPortalView.as_view(), name='portal-facility'),
    path('portal/facility/beds/', FacilityBedsPortalView.as_view(), name='portal-facility-beds'),

    # ─── Doctor portal ────────────────────────────────────────────────────────
    path('portal/doctor/', DoctorPortalView.as_view(), name='portal-doctor'),
    path('portal/doctor/status/', DoctorStatusPortalView.as_view(), name='portal-doctor-status'),

    # ─── Admin portal ─────────────────────────────────────────────────────────
    path('portal/admin/users/', AdminUserListView.as_view(), name='portal-admin-users'),
    path('portal/admin/users/<int:pk>/', AdminUserDetailView.as_view(), name='portal-admin-user-detail'),
]

