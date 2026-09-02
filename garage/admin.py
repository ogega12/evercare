from django.contrib import admin
from .models import Service, Promotion, GalleryImage, Testimonial, Booking, ContactMessage

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'featured', 'created_at')
    search_fields = ('name', 'short_description', 'description')
    list_filter = ('featured', 'created_at')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'discount', 'price', 'start_date', 'end_date', 'active')
    list_filter = ('active', 'start_date')
    search_fields = ('title', 'description')

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title', 'caption')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'approved', 'date')
    list_filter = ('approved', 'rating', 'date')
    search_fields = ('name', 'review')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'vehicle_registration', 'service', 'custom_service', 'preferred_date', 'status', 'created_at')
    list_filter = ('status', 'preferred_date', 'created_at')
    search_fields = ('full_name', 'phone', 'vehicle_registration', 'custom_service')
    readonly_fields = ('created_at',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
