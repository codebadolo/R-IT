from django.contrib import admin
from .models import *
from .forms import ProductFormAdmin, AttributeValueInlineForm
from django.contrib.auth.models import Group
from django.utils.html import format_html

# Super Admin Site Customization
class SuperAdminSite(admin.AdminSite):
    site_header = 'Super Admin Dashboard'
    site_title = 'Super Admin Panel'
    index_title = 'Manage Your Store'

    def has_permission(self, request):
        return request.user.is_authenticated and request.user.is_superuser

super_admin_site = SuperAdminSite(name='superadminsite')

# Industry Management
@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}

# Category & Subcategory
class SubCategoryInline(admin.TabularInline):
    model = SubCategories
    extra = 1

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'created_at')
    list_filter = ('industry',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SubCategoryInline]
    search_fields = ['name', 'industry__name']  # Add search fields

super_admin_site.register(Categories, CategoriesAdmin)  # Register with super_admin_site

@admin.register(SubCategories)
class SubCategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'categories', 'created_at')
    list_filter = ('categories__industry', 'categories')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'categories__name']  # Add search fields

super_admin_site.register(SubCategories, SubCategoriesAdmin)  # Register with super_admin_site

# Product Attribute Management
class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 1

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    inlines = [AttributeValueInline]

class ProductTypeAttributeInline(admin.TabularInline):
    model = ProductTypeAttribute
    extra = 1

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    inlines = [ProductTypeAttributeInline]

# Product Inventory Management
class ProductInventoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'total_quantity', 'available_quantity', 'created_at']
    search_fields = ['product__title']

super_admin_site.register(ProductInventory, ProductInventoryAdmin)

# Product Management
class ProductImages(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAditionalInformations(admin.TabularInline):
    model = ProductAditionalInformation
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    form = ProductFormAdmin
    inlines = [
        ProductImages,
        ProductAditionalInformations,
        AttributeValueInline,
        ProductTypeAttributeInline
    ]
    list_display = ['thumbnail', 'title', 'regular_price', 'discounted_price', 'brand', 'product_type', 'categories']
    list_filter = ['categories__industry', 'categories', 'subcategories', 'brand', 'product_type']
    search_fields = ['title', 'brand__name', 'product_type__name']
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['categories', 'subcategories']  # Ensure this line is here

    def thumbnail(self, obj):
        image = obj.productimage_set.first()
        if image:
            return format_html('<img src="{}" width="100" height="100" style="border-radius: 5px;" />', image.image)
        return format_html('<img src="https://placehold.co/50x50" width="50" height="50" style="border-radius: 5px;" />')

    thumbnail.short_description = 'Image'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subcategories":
            if request.resolver_match.kwargs.get('object_id'):
                product_id = request.resolver_match.kwargs['object_id']
                product = Product.objects.get(pk=product_id)
                kwargs["queryset"] = SubCategories.objects.filter(categories=product.categories)
            else:
                kwargs["queryset"] = SubCategories.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    class Media:
        js = ('admin-panel/assets/js/custom_admin.js',)

super_admin_site.register(Product, ProductAdmin)

# Miscellaneous
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['product', 'user']

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