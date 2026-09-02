from django.urls import path
from . import views

app_name = 'garage'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('services/', views.ServiceListView.as_view(), name='services'),
    path('services/<slug:slug>/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('gallery/', views.GalleryView.as_view(), name='gallery'),
    path('offers/', views.PromotionsView.as_view(), name='offers'),
    path('booking/', views.BookingCreateView.as_view(), name='booking'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('admin-dashboard/login/', views.AdminLoginView.as_view(), name='admin_login'),
    path('admin-dashboard/logout/', views.AdminLogoutView.as_view(), name='admin_logout'),
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
]
