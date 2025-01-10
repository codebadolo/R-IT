from django.contrib import admin
from .models import *
from unfold.admin import ModelAdmin  , TabularInline
from .forms import ProductFormAdmin, AttributeValueInlineForm
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.urls import path
from django.http import JsonResponse
from unfold.sites import UnfoldAdminSite
# Super Admin Site Customization
class SuperAdminSite(UnfoldAdminSite):
    site_header = 'Super Admin Dashboard'
    site_title = 'Super Admin Panel'
    index_title = 'Manage Your Store'

    def has_permission(self, request):
        return request.user.is_authenticated and request.user.is_superuser

super_admin_site = SuperAdminSite(name='superadminsite')

# Industry Management
@admin.register(Industry)
class IndustryAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}

# Category & Subcategory
class SubCategoryInline(TabularInline):
    model = SubCategories
    extra = 1

@admin.register(Categories)
class CategoriesAdmin(ModelAdmin):
    list_display = ('name', 'industry', 'created_at')
    list_filter = ('industry',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SubCategoryInline]
    search_fields = ['name', 'industry__name']  # Add search fields

super_admin_site.register(Categories, CategoriesAdmin)  # Register with super_admin_site

@admin.register(SubCategories)
class SubCategoriesAdmin(ModelAdmin):
    list_display = ('name', 'categories', 'created_at')
    list_filter = ('categories__industry', 'categories')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'categories__name']  # Add search fields

super_admin_site.register(SubCategories, SubCategoriesAdmin)  # Register with super_admin_site

# Product Attribute Management
class AttributeValueInline(TabularInline):
    model = AttributeValue
    extra = 1

@admin.register(Attribute)
class AttributeAdmin(ModelAdmin):
    inlines = [AttributeValueInline]

class ProductTypeAttributeInline(TabularInline):
    model = ProductTypeAttribute
    extra = 1

@admin.register(ProductType)
class ProductTypeAdmin(ModelAdmin):
    list_display = ('name', 'created_at')
    inlines = [ProductTypeAttributeInline]

# Product Inventory Management
class ProductInventoryAdmin(ModelAdmin):
    list_display = ['product', 'total_quantity', 'available_quantity', 'created_at']
    search_fields = ['product__title']

super_admin_site.register(ProductInventory, ProductInventoryAdmin)

# Product Management
class ProductImages(TabularInline):
    model = ProductImage
    extra = 1

class ProductAditionalInformations(TabularInline):
    model = ProductAditionalInformation
    extra = 1
    

        
class ProductAdmin(ModelAdmin):
    form = ProductFormAdmin
    inlines = [ProductImages, ProductAditionalInformations, AttributeValueInline, ProductTypeAttributeInline]
    list_display = ['thumbnail', 'title', 'regular_price', 'discounted_price', 'brand', 'product_type', 'categories']
    list_filter = ['categories__industry', 'categories', 'subcategories', 'brand', 'product_type']
    search_fields = ['title', 'brand__name', 'product_type__name']
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['categories', 'subcategories']
    change_form_template = 'admin/products/product/change_form.html'

    class Media:
        js = ('custom_admin/custom_script.js',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('subcategories_by_category/', self.admin_site.admin_view(self.subcategories_by_category), name='subcategories_by_category')
        ]
        return custom_urls + urls

    def subcategories_by_category(self, request):
        category_id = request.GET.get('category_id')
        subcategories = SubCategories.objects.filter(categories_id=category_id).values('id', 'name')
        return JsonResponse({'subcategories': list(subcategories)})

    def thumbnail(self, obj):
        image = obj.productimage_set.first()
        if image:
            return format_html('<img src="{}" width="100" height="100" style="border-radius: 5px;" />', image.image)
        return format_html('<img src="https://placehold.co/50x50" width="50" height="50" style="border-radius: 5px;" />')

    thumbnail.short_description = 'Image'
super_admin_site.register(Product, ProductAdmin)

# Miscellaneous
class CartModelAdmin(ModelAdmin):
    list_display = ['product_thumbnail', 'product', 'user']
    readonly_fields = ['product_thumbnail','product', 'user']

    def product_thumbnail(self, obj):
        image = obj.product.productimage_set.first()
        if image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', image.image)
        return format_html('<img src="https://placehold.co/50x50" width="50" height="50" style="border-radius: 5px;" />')

    product_thumbnail.short_description = 'Product Image'

from django.contrib import admin
from .models import *

# Customize the Admin panel
class CustomerAddressAdmin(ModelAdmin):
    list_display = ['user', 'street_address', 'city', 'state', 'zip_code', 'country', 'mobile', 'is_shipping', 'is_billing']
    search_fields = ['user__username', 'city', 'state']
    list_filter = ['is_shipping', 'is_billing']

@admin.register(PlacedOder)
class PlacedOderAdmin(ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'shipping_address', 'tracking_number', 'estimated_delivery_date', 'sub_total_price', 'paid', 'placed_date']
    search_fields = ['order_number', 'user__username', 'status', 'tracking_number']
    list_filter = ['status', 'paid']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('update_shipping_status/<int:order_id>/', self.admin_site.admin_view(self.update_shipping_status), name='update_shipping_status')
        ]
        return custom_urls + urls

    def update_shipping_status(self, request, order_id):
        # Implement functionality to update shipping status
        pass
# Register models to the super admin site
#super_admin_site.register(CustomerAddress, CustomerAddressAdmin)
#super_admin_site.register(PlacedOder, PlacedOderAdmin)
#super_admin_site.register(Cart, CartModelAdmin)
#super_admin_site.register(Cart, CartModelAdmin)

super_admin_site.register(Industry)

super_admin_site.register(Cart, CartModelAdmin)
super_admin_site.register(ProductImage)
super_admin_site.register(ProductAditionalInformation)
super_admin_site.register(CuponCodeGenaration)
super_admin_site.register(CustomerAddress)
super_admin_site.register(PlacedOder)
super_admin_site.register(PlacedeOderItem)
super_admin_site.register(CompletedOder)
super_admin_site.register(CompletedOderItems)
super_admin_site.register(ProductStarRatingAndReview)
super_admin_site.register(Group)