from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Consultation
from datetime import date, time, timedelta


class ConsultationModelTest(TestCase):
    """Test cases for Consultation model"""
    
    def setUp(self):
        self.consultation = Consultation.objects.create(
            full_name="Test User",
            email="test@example.com",
            phone="+1234567890",
            company="Test Company",
            project_type="web_development",
            budget="10k-25k",
            timeline="1-3_months",
            preferred_date=date.today() + timedelta(days=7),
            preferred_time=time(10, 0),
            timezone="IST",
            message="Test consultation request"
        )
    
    def test_consultation_creation(self):
        """Test that consultation is created properly"""
        self.assertEqual(self.consultation.full_name, "Test User")
        self.assertEqual(self.consultation.email, "test@example.com")
        self.assertEqual(self.consultation.status, "pending")
    
    def test_is_upcoming(self):
        """Test is_upcoming method"""
        self.assertTrue(self.consultation.is_upcoming())
    
    def test_string_representation(self):
        """Test string representation"""
        expected = f"Test User - web_development ({self.consultation.preferred_date})"
        self.assertEqual(str(self.consultation), expected)


class ConsultationAPITest(APITestCase):
    """Test cases for Consultation API"""
    
    def test_create_consultation(self):
        """Test creating a consultation via API"""
        url = reverse('consultation-list')
        data = {
            'full_name': 'API Test User',
            'email': 'apitest@example.com',
            'phone': '+9876543210',
            'company': 'API Test Company',
            'project_type': 'mobile_app',
            'budget': '25k-50k',
            'timeline': '3-6_months',
            'preferred_date': (date.today() + timedelta(days=10)).isoformat(),
            'preferred_time': '14:00',
            'timezone': 'IST',
            'message': 'API test consultation'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Consultation.objects.count(), 1)
        self.assertEqual(Consultation.objects.get().full_name, 'API Test User')
    
    def test_list_consultations(self):
        """Test listing consultations"""
        url = reverse('consultation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)