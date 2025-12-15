from rest_framework import serializers
from .models import Consultation
from datetime import date

class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'status']
    
    def validate_email(self, value):
        """Validate email format"""
        if not '@' in value:
            raise serializers.ValidationError("Enter a valid email address.")
        return value.lower()
    
    def validate_preferred_date(self, value):
        """Ensure date is not in the past"""
        if value < date.today():
            raise serializers.ValidationError("Preferred date cannot be in the past.")
        return value
    
    def validate(self, data):
        """Custom validation"""
        # Check for duplicate bookings
        if Consultation.objects.filter(
            email=data.get('email'),
            preferred_date=data.get('preferred_date'),
            preferred_time=data.get('preferred_time'),
            status__in=['pending', 'confirmed']
        ).exists():
            raise serializers.ValidationError(
                "You already have a consultation booked for this time."
            )
        return data