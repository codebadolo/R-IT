from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
from .forms import ProductFormAdmin
# Register your models here.

class SuperAdminSite(admin.AdminSite):
    site_header = 'Super Admin Dashboard'
    site_title = 'Super Admin Dashboard'
    index_title = 'Control Your Site From Here'

    def has_permission(self, request):
        # Check if the user is authenticated and has the role "Admin" (user_role == 1)
        return request.user.is_authenticated and request.user.is_superuser

    login_view = 'superadmin:login'  # The URL name for the default admin login view

super_admin_site = SuperAdminSite(name='superadminsite')

# Industry Admin
@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    
# SubCategories Inline (to show in Category Admin)
class SubCategoryInline(admin.TabularInline):
    model = SubCategories
    extra = 1  # Number of empty forms to display
# Categories Admin
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'created_at')
    list_filter = ('industry',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SubCategoryInline]  # Attach SubCategories inline   
    
    
# SubCategories Admin
@admin.register(SubCategories)
class SubCategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'categories', 'created_at')
    list_filter = ('categories__industry', 'categories')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}  
      
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['product', 'user']

# Register Cart model with CartModelAdmin
#super_admin_site.register(Cart, CartModelAdmin)

class ProductImages(admin.TabularInline):
    model = ProductImage

class ProductInventoryInline(admin.StackedInline):  # Use StackedInline for better layout
    model = ProductInventory
    extra = 1
    
class ProductAditionalInformations(admin.TabularInline):
    model = ProductAditionalInformation

class ProductTypeAttributeInline(admin.TabularInline):
    model = ProductTypeAttribute
    extra = 1

class ProductInventoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'total_quantity', 'available_quantity', 'created_at']
    search_fields = ['product__title']  # Search by product title

super_admin_site.register(ProductInventory, ProductInventoryAdmin)

from django.utils.html import format_html
class ProductAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/admin_subcategories_filter.js',) 
    form = ProductFormAdmin
    inlines = [
        ProductTypeAttributeInline,
    ]
    list_display = ['thumbnail', 'title', 'regular_price', 'discounted_price', 'brand', 'product_type', 'categories']
    list_filter = ['categories__industry','categories', 'brand', 'product_type']
    search_fields = ['title', 'brand__name', 'product_type__name']
    filter_horizontal = ('attributes',)
    prepopulated_fields = {'slug': ('title',)}

    def thumbnail(self, obj):
        # Get the first image for the product or use a placeholder
        image = obj.productimage_set.first()
        if image:
            return format_html('<img src="{}" width="100" height="100" style="border-radius: 5px;" />', image.image)
        else:
            return format_html('<img src="https://placehold.co/50x50" width="50" height="50" style="border-radius: 5px;" />')

    thumbnail.short_description = 'Image'
    
    def categories(self, obj):
        if obj.categories:
            subcategories = obj.categories.subcategories.all()
            return ", ".join([sub.name for sub in subcategories])
        return "No Category"

'''    def categories(self, obj):
        if obj.categories:
            subcategories = obj.categories.subcategories.all()  # Use .subcategories if related_name exists
            return ", ".join([sub.name for sub in subcategories])
        return "No Category"'''

 # Add custom JS for filtering subcategories dynamically
'''class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductTypeAttributeInline,
    ]
    list_display = ['title', 'regular_price', 'discounted_price', 'brand', 'product_type', 'categories']
    list_filter = ['categories', 'brand', 'product_type']
    search_fields = ['title', 'brand__name', 'product_type__name']
    
    # If attributes are now a ManyToMany field
    filter_horizontal = ('attributes',)'''

#super_admin_site.register(Product, ProductAdmin)


#uper_admin_site.register(Product, ProductAdmin)

super_admin_site.register(Product, ProductAdmin)

# Register other models
super_admin_site.register(Industry)
super_admin_site.register(Categories)
super_admin_site.register(SubCategories)
super_admin_site.register(ProductImage)
super_admin_site.register(ProductAditionalInformation)
super_admin_site.register(Cart, CartModelAdmin)
super_admin_site.register(CustomerAddress)
super_admin_site.register(PlacedOder)
super_admin_site.register(PlacedeOderItem)
super_admin_site.register(CuponCodeGenaration)
super_admin_site.register(CompletedOder)
super_admin_site.register(CompletedOderItems)
super_admin_site.register(ProductStarRatingAndReview)
super_admin_site.register(Group)
