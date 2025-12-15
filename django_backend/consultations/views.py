from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.conf import settings
from .models import Consultation
from .serializers import ConsultationSerializer

class ConsultationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for consultation bookings
    """
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    permission_classes = [AllowAny]  # Change to IsAuthenticated for admin-only access
    
    def create(self, request, *args, **kwargs):
        """Create new consultation booking"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Send confirmation email
        self.send_confirmation_email(serializer.instance)
        
        # Send notification to admin
        self.send_admin_notification(serializer.instance)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    def send_confirmation_email(self, consultation):
        """Send confirmation email to client"""
        subject = f"Consultation Confirmed - {consultation.preferred_date}"
        message = f"""
        Dear {consultation.full_name},
        
        Thank you for booking a consultation with Agency.io!
        
        Your consultation details:
        - Date: {consultation.preferred_date}
        - Time: {consultation.preferred_time} {consultation.timezone}
        - Project Type: {consultation.get_project_type_display()}
        
        We'll send you a meeting link 24 hours before the scheduled time.
        
        If you need to reschedule, please reply to this email.
        
        Best regards,
        Agency.io Team
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [consultation.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send confirmation email: {e}")
    
    def send_admin_notification(self, consultation):
        """Send notification to admin about new booking"""
        subject = f"New Consultation Booking - {consultation.full_name}"
        message = f"""
        New consultation booking received:
        
        Client: {consultation.full_name}
        Email: {consultation.email}
        Phone: {consultation.phone}
        Company: {consultation.company or 'N/A'}
        
        Project Type: {consultation.get_project_type_display()}
        Budget: {consultation.get_budget_display()}
        Timeline: {consultation.get_timeline_display()}
        
        Scheduled: {consultation.preferred_date} at {consultation.preferred_time} {consultation.timezone}
        
        Message:
        {consultation.message}
        
        View in admin panel: {settings.SITE_URL}/admin/consultations/consultation/{consultation.id}/
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send admin notification: {e}")
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm a consultation booking"""
        consultation = self.get_object()
        consultation.status = 'confirmed'
        consultation.save()
        return Response({'status': 'Consultation confirmed'})
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a consultation booking"""
        consultation = self.get_object()
        consultation.status = 'cancelled'
        consultation.save()
        return Response({'status': 'Consultation cancelled'})