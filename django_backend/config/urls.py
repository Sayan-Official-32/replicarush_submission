"""
URL configuration for consultation booking project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        'message': 'Consultation Booking API',
        'version': '1.0',
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/',
            'consultations': '/api/consultations/',
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('consultations.urls')),
    path('', api_root),
]