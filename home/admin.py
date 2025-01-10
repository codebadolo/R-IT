from django.contrib import admin
from products.admin import super_admin_site
from django.contrib import admin
from .models import  NewArrival, CustomerReview, FlashSale, FeaturedCategory, BlogHighlight, NewsletterSignup
from . models import SliderArea, DisplayHotProductInCategories, PopularCategories
# Register your models here.
from unfold.admin import ModelAdmin  , TabularInline
# Register New Models for Admin
class NewArrivalAdmin(admin.ModelAdmin):
    list_display = ('product', 'arrival_date')

class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')

class FlashSaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'discount_percentage', 'start_date', 'end_date')

class FeaturedCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'featured_date')

class BlogHighlightAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')

class NewsletterSignupAdmin(admin.ModelAdmin):
    list_display = ('email', 'signup_date')

super_admin_site.register(NewArrival, NewArrivalAdmin)
super_admin_site.register(CustomerReview, CustomerReviewAdmin)
super_admin_site.register(FlashSale, FlashSaleAdmin)
super_admin_site.register(FeaturedCategory, FeaturedCategoryAdmin)
super_admin_site.register(BlogHighlight, BlogHighlightAdmin)
super_admin_site.register(NewsletterSignup, NewsletterSignupAdmin)
super_admin_site.register(SliderArea)
super_admin_site.register(DisplayHotProductInCategories)
super_admin_site.register(PopularCategories)

