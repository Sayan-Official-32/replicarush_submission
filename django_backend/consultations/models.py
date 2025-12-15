from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from django.utils import timezone

class Consultation(models.Model):
    """Model to store consultation booking requests"""
    
    # Personal Information
    full_name = models.CharField(max_length=200)
    email = models.EmailField(validators=[EmailValidator()])
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17)
    company = models.CharField(max_length=200, blank=True, null=True)
    
    # Project Details
    PROJECT_TYPES = [
        ('web_development', 'Web Development'),
        ('mobile_app', 'Mobile App'),
        ('ai_ml', 'AI/ML Solution'),
        ('ecommerce', 'E-commerce Platform'),
        ('enterprise', 'Enterprise Software'),
        ('consulting', 'Technical Consulting'),
        ('other', 'Other'),
    ]
    project_type = models.CharField(max_length=50, choices=PROJECT_TYPES)
    
    BUDGET_RANGES = [
        ('5k-10k', '$5,000 - $10,000'),
        ('10k-25k', '$10,000 - $25,000'),
        ('25k-50k', '$25,000 - $50,000'),
        ('50k-100k', '$50,000 - $100,000'),
        ('100k+', '$100,000+'),
    ]
    budget = models.CharField(max_length=20, choices=BUDGET_RANGES)
    
    TIMELINE_CHOICES = [
        ('urgent', 'Urgent (1-2 weeks)'),
        ('1-3_months', '1-3 months'),
        ('3-6_months', '3-6 months'),
        ('6+_months', '6+ months'),
        ('flexible', 'Flexible'),
    ]
    timeline = models.CharField(max_length=20, choices=TIMELINE_CHOICES)
    
    # Schedule
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    timezone = models.CharField(max_length=10, default='IST')
    
    # Message
    message = models.TextField()
    
    # Status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True, help_text="Internal notes")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Consultation'
        verbose_name_plural = 'Consultations'
    
    def __str__(self):
        return f"{self.full_name} - {self.project_type} ({self.preferred_date})"
    
    def is_upcoming(self):
        """Check if consultation is in the future"""
        return self.preferred_date >= timezone.now().date()