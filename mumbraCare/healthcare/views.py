from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Advertisement, BedStatus, Doctor, HealthcareFacility, Pharmacy, SiteSettings
from .serializers import (
    DoctorSerializer,
    DoctorStatusUpdateSerializer,
    HealthcareFacilitySerializer,
    PharmacySerializer,
)


class FacilityListView(generics.ListAPIView):
    """GET /api/facilities/ — list all active healthcare facilities.

    Filter by: area, facility_type, is_verified
    Search by: name, address
    """

    serializer_class = HealthcareFacilitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['area', 'facility_type', 'is_verified']
    search_fields = ['name', 'address']
    ordering_fields = ['name', 'area']

    def get_queryset(self):
        return (
            HealthcareFacility.objects.filter(is_active=True)
            .select_related('bed_status')
            .prefetch_related('doctors')
        )


class FacilityDetailView(generics.RetrieveAPIView):
    """GET /api/facilities/<pk>/ — detail of a single facility."""

    serializer_class = HealthcareFacilitySerializer
    queryset = HealthcareFacility.objects.filter(is_active=True).select_related('bed_status')


class BedTrackerView(generics.ListAPIView):
    """GET /api/beds/ — real-time bed availability, optionally filtered by area.

    The 'Green Means Ready' dashboard endpoint.
    Filter by: area (via facility__area)
    """

    serializer_class = HealthcareFacilitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'facility__area': ['exact'], 'available_beds': ['gt', 'gte']}

    def get_queryset(self):
        return (
            HealthcareFacility.objects.filter(is_active=True)
            .select_related('bed_status')
        )

    def list(self, request, *args, **kwargs):
        area = request.query_params.get('area')
        qs = HealthcareFacility.objects.filter(is_active=True).select_related('bed_status')
        if area:
            qs = qs.filter(area=area.upper())
        serializer = HealthcareFacilitySerializer(qs, many=True)
        return Response(serializer.data)


class DoctorListView(generics.ListAPIView):
    """GET /api/doctors/ — directory of doctors.

    Filter by: specialty, is_available, facility__area
    Search by: name
    """

    serializer_class = DoctorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['specialty', 'is_available', 'facility__area']
    search_fields = ['name']

    def get_queryset(self):
        return Doctor.objects.select_related('facility').all()


class DoctorStatusUpdateView(generics.UpdateAPIView):
    """PATCH /api/doctors/<pk>/status/ — toggle doctor availability (volunteer/staff use)."""

    serializer_class = DoctorStatusUpdateSerializer
    queryset = Doctor.objects.all()
    http_method_names = ['patch']


class PharmacyListView(generics.ListAPIView):
    """GET /api/pharmacies/ — night pharmacy directory.

    Filter by: area, is_24_7, is_verified
    """

    serializer_class = PharmacySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['area', 'is_24_7', 'is_verified']
    search_fields = ['name', 'address']

    def get_queryset(self):
        return Pharmacy.objects.filter(is_active=True)


@api_view(['GET'])
def health_check(request):
    """GET /api/health/ — simple liveness probe."""
    return Response({'status': 'ok', 'service': 'Mumbra Care API'})


class PublicAdsView(APIView):
    """GET /api/ads/ — returns active advertisements for the rotating banner."""
    permission_classes = [AllowAny]

    def get(self, request):
        ads = Advertisement.objects.filter(is_active=True)
        data = [
            {
                'id': ad.id,
                'text': ad.text,
                'image': request.build_absolute_uri(ad.image.url) if ad.image else None,
                'link_url': ad.link_url,
            }
            for ad in ads
        ]
        return Response(data)


class PublicSettingsView(APIView):
    """GET /api/site-settings/ — returns donate QR and related config."""
    permission_classes = [AllowAny]

    def get(self, request):
        obj = SiteSettings.objects.first()
        if not obj:
            return Response({'paytm_qr_image': None, 'donate_name': 'Mumbra Care', 'donate_upi_id': ''})
        return Response({
            'paytm_qr_image': request.build_absolute_uri(obj.paytm_qr_image.url) if obj.paytm_qr_image else None,
            'donate_name': obj.donate_name,
            'donate_upi_id': obj.donate_upi_id,
        })

