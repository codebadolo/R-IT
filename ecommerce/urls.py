from django.contrib import admin
from django.urls import path, include
from AdminPanel.admin import employee_Management_admin_site
from Vendors.admin import vendor_admin_site
from products.admin import super_admin_site
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('super-admin/', super_admin_site.urls),
    path('employee-dashboard/', employee_Management_admin_site.urls),
    path('vendor-dashboard/', vendor_admin_site.urls),
]

urlpatterns += i18n_patterns(
    path('', include('home.urls')),
      path('i18n/', include('django.conf.urls.i18n')),  # Add this line
    path('', include("accounts.urls")),
    path('', include('products.urls')),
    
    path('', include('AdminPanel.urls')),
    path('', include('Vendors.urls')),
    path('', include('payments.urls')),
  
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)