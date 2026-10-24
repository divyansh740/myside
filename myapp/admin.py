from django.contrib import admin
from .models import Course, Enrollment, EmailOTP, Enquiry

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'course')
    search_fields = ('full_name', 'phone', 'email')
    list_filter = ('course',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course') # Isme se 'enrolled_at' hata diya
    list_filter = ('course',)

admin.site.register(Course)
admin.site.register(EmailOTP)