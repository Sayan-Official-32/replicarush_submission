from django.contrib import admin
from .models import Consultation

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'email', 'company', 'project_type',
        'preferred_date', 'preferred_time', 'status', 'created_at'
    ]
    list_filter = ['status', 'project_type', 'budget', 'timeline', 'created_at']
    search_fields = ['full_name', 'email', 'company', 'message']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('full_name', 'email', 'phone', 'company')
        }),
        ('Project Details', {
            'fields': ('project_type', 'budget', 'timeline', 'message')
        }),
        ('Schedule', {
            'fields': ('preferred_date', 'preferred_time', 'timezone')
        }),
        ('Status', {
            'fields': ('status', 'notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_confirmed', 'mark_as_completed', 'mark_as_cancelled']
    
    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
    mark_as_confirmed.short_description = "Mark selected as Confirmed"
    
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_as_completed.short_description = "Mark selected as Completed"
    
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
    mark_as_cancelled.short_description = "Mark selected as Cancelled"