from django.contrib import admin
from .models import VendorStore
from products.models import Product, ProductImage, ProductAditionalInformation, PlacedOder, CompletedOder, PlacedeOderItem, CompletedOderItems
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.html import format_html
from .adminForms import ProductModelAdminForm
# Vendor Admin Site
# In Vendors/admin.py

# In Vendors/admin.py

from django.urls import path
from django.template.response import TemplateResponse
from datetime import datetime, timedelta
from products.models import Cart, PlacedOder, CompletedOder

class CustomVendorAdminSite(admin.AdminSite):
    site_header = 'MVEC Seller Dashboard'
    site_title = 'Seller Dashboard'
    index_title = 'List Your Product And Earn Money'

    def has_permission(self, request):
        return request.user.is_authenticated and request.user.user_role == '3'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.vendor_dashboard), name='vendor_dashboard'),
        ]
        return custom_urls + urls

    def vendor_dashboard(self, request):
        vendor_store = VendorStore.objects.filter(user=request.user).first()
        products = Product.objects.filter(vendor_stores=vendor_store)
        
        # Calculate statistics
        customers_with_cart = Cart.objects.filter(product__vendor_stores=vendor_store).values('user').distinct().count()
        total_orders = PlacedOder.objects.filter(user=request.user).count()
        total_completed_orders = CompletedOder.objects.filter(user=request.user).count()
        last_30_days = datetime.now() - timedelta(days=30)
        orders_last_30_days = PlacedOder.objects.filter(user=request.user, placed_date__gte=last_30_days).count()
        
        # Financial metrics
        total_revenue = CompletedOder.objects.filter(user=request.user).aggregate(models.Sum('sub_total_price'))['sub_total_price__sum'] or 0
        
        context = {
            'vendor_store': vendor_store,
            'products': products,
            'customers_with_cart': customers_with_cart,
            'total_orders': total_orders,
            'total_completed_orders': total_completed_orders,
            'orders_last_30_days': orders_last_30_days,
            'total_revenue': total_revenue,
        }
        return TemplateResponse(request, 'admin/vendor_dashboard.html', context)

vendor_admin_site = CustomVendorAdminSite(name='vendor_admin_site')

# ModelAdmin For VendorStore
class VendorStoreModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'logo', 'cover_photo')}),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if VendorStore.objects.filter(user=request.user).count() < 3:
            obj.user = request.user
            obj.save()
            super().save_model(request, obj, form, change)
        else:
            messages.info(request, f"{request.user} can't create more than 3 Stores")
            return redirect('/vendor-dashboard/Vendors/vendorstore/')

# TabularInline For Product Model
class ProductImageTabular(admin.TabularInline):
    model = ProductImage
    extra = 0

class ProductAditonalInformationTabular(admin.TabularInline):
    model = ProductAditionalInformation
    extra = 0

# ModelAdmin For Product Model
class ProductModelAdmin(admin.ModelAdmin):
    form = ProductModelAdminForm
    inlines = (ProductImageTabular, ProductAditonalInformationTabular)
    list_display = ('title', 'formated_stoc', 'discounted_price', 'categories', 'vendor_stores', 'sort_descriptions')
    list_editable = ('categories', 'vendor_stores')
    readonly_fields = ['slug']
    list_filter = ('vendor_stores',)

    fieldsets = [
        ('Product Identity', {'fields': ['title', 'slug', 'vendor_stores']}),
        ('Prices & Stock', {'classes': ('collapse',), 'fields': [('regular_price', 'discounted_parcent', 'stoc', 'out_of_stoc')]}),
        ('Descriptions', {'classes': ('collapse',), 'fields': [('modle', 'tag', 'categories'), 'description']}),
        ('Details Description', {'fields': ['details_description']}),
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.user = request.user
        form.request = request
        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_authenticated:
            try:
                vendor_store = VendorStore.objects.filter(user=request.user)
                qs = qs.filter(vendor_stores__in=vendor_store)
            except VendorStore.DoesNotExist:
                return qs.none()
        return qs

    @admin.display(description='Description')
    def sort_descriptions(self, obj):
        return obj.description.replace('<p>', '').replace('</p>', '')[:30]

    @admin.display(description='Stock Product')
    def formated_stoc(self, obj):
        return format_html('<strong style="color:#008000;">{}</strong>', obj.stoc)
    
    formated_stoc.short_description = "Available in Stock"

    def save_model(self, request, obj, form, change):
        if request.user.user_role == '3':
            obj.save()
        return super().save_model(request, obj, form, change)

# Register models with custom admin site
vendor_admin_site.register(VendorStore, VendorStoreModelAdmin)
vendor_admin_site.register(Product, ProductModelAdmin)

# Register order models
class PlacedOrderModelAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'shipping_status', 'placed_date')
    list_filter = ('status', 'shipping_status', 'placed_date')
    search_fields = ('order_number', 'user__email')

class CompletedOrderModelAdmin(admin.ModelAdmin):
    list_display = ('oder_number', 'user', 'status', 'complete_date')
    list_filter = ('status', 'complete_date')
    search_fields = ('oder_number', 'user__email')

vendor_admin_site.register(PlacedOder, PlacedOrderModelAdmin)
vendor_admin_site.register(CompletedOder, CompletedOrderModelAdmin)

# Register the custom admin site
admin.site.register(VendorStore)