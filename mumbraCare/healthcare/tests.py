from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from healthcare.models import Doctor, HealthcareFacility, Pharmacy
from healthcare.serializers import PortalUserCreateSerializer


class PortalSecurityTests(APITestCase):
	def setUp(self):
		self.facility = HealthcareFacility.objects.create(
			name='Test Facility',
			facility_type='HOSPITAL',
			area='KAUSA',
			address='Test Address',
			contact_number='1234567890',
		)
		self.doctor = Doctor.objects.create(
			name='Test Doctor',
			specialty='GENERAL',
			facility=self.facility,
			contact_number='1234567890',
		)

	def test_public_doctor_status_update_requires_authentication(self):
		response = self.client.patch(
			f'/api/doctors/{self.doctor.pk}/status/',
			{'is_available': False},
			format='json',
		)
		self.assertIn(response.status_code, {status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN})


class PortalUserSerializerTests(APITestCase):
	def setUp(self):
		self.facility = HealthcareFacility.objects.create(
			name='Admin Facility',
			facility_type='HOSPITAL',
			area='KAUSA',
			address='Facility Address',
			contact_number='1111111111',
		)
		self.pharmacy = Pharmacy.objects.create(
			name='Test Pharmacy',
			area='STATION_ROAD',
			address='Pharmacy Address',
			contact_number='2222222222',
		)

	def test_non_admin_portal_user_must_be_linked(self):
		serializer = PortalUserCreateSerializer(data={
			'username': 'orphan',
			'email': 'orphan@example.com',
			'password': 'pass87654',
			'is_staff': False,
		})
		self.assertFalse(serializer.is_valid())
		self.assertIn('non_field_errors', serializer.errors)

	def test_admin_can_create_pharmacy_portal_user(self):
		serializer = PortalUserCreateSerializer(data={
			'username': 'pharmacyuser',
			'email': 'pharmacy@example.com',
			'password': 'pass87654',
			'link_to_pharmacy': self.pharmacy.pk,
			'is_staff': False,
		})
		self.assertTrue(serializer.is_valid(), serializer.errors)
		user = serializer.save()
		self.pharmacy.refresh_from_db()
		self.assertEqual(self.pharmacy.user_id, user.id)


class PharmacyPortalTests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username='pharmacyowner',
			email='owner@example.com',
			password='pass87654',
		)
		self.pharmacy = Pharmacy.objects.create(
			name='Portal Pharmacy',
			area='KAUSA',
			address='Portal Address',
			contact_number='3333333333',
			user=self.user,
		)
		self.client.force_authenticate(self.user)

	def test_me_view_returns_pharmacy_role(self):
		response = self.client.get('/api/auth/me/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['user_type'], 'PHARMACY')
		self.assertEqual(response.data['profile_id'], self.pharmacy.id)

	def test_pharmacy_portal_updates_own_profile(self):
		response = self.client.patch('/api/portal/pharmacy/', {
			'contact_number': '4444444444',
			'is_24_7': True,
		}, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.pharmacy.refresh_from_db()
		self.assertEqual(self.pharmacy.contact_number, '4444444444')
		self.assertTrue(self.pharmacy.is_24_7)
