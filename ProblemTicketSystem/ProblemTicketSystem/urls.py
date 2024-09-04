from django.contrib import admin
from django.urls import path, include
from . import views  # Import custom views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('consumer.urls')),  # Includes consumer app URLs
    path('secondadmin/', include('control.urls')),  # Includes control app URLs
]

# Custom 404 handler
handler404 = 'ProblemTicketSystem.views.custom_page_not_found'
