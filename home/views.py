from .models import  (
    SliderArea, DisplayHotProductInCategories, PopularCategories , 
    NewArrival, CustomerReview, FlashSale, FeaturedCategory, BlogHighlight, NewsletterSignup 
)
from django.http import HttpResponse
from django.shortcuts import render, redirect
from products.models import (
    ProductBrand, Attribute, AttributeValue,
    Product, Categories, ProductType, SubCategories ,Industry, Cart  )
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.db.models import Q
from django.core.paginator import Paginator
from Vendors.models import VendorStore

def home(request):
    sub_total = 0.00
    carts = ""
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
        if carts:
            sub_total = Cart.subtotal_product_price(user=request.user)
    
    slider = SliderArea.objects.all()
    industry = Industry.objects.all()
    hot_products_in_cate = DisplayHotProductInCategories.objects.all()[:4]
    trending_product = Product.objects.all()
    trending_division_title = "Trending Product"
    popular_categories = PopularCategories.objects.all()
    new_arrivals = NewArrival.objects.all()[:10]  # Fetch the latest 10 new arrivals
    customer_reviews = CustomerReview.objects.all()[:10]  # Fetch the latest 10 customer reviews
    flash_sales = FlashSale.objects.all()  # Fetch all ongoing flash sales
    featured_categories = FeaturedCategory.objects.all()
    blog_highlights = BlogHighlight.objects.all()[:5]  # Fetch the latest 5 blog highlights
    newsletter_signup = NewsletterSignup.objects.all()  # Fetch all newsletter signups (for admin purposes)
        # Filter categories to only include those with related products
    industries_with_products = Industry.objects.annotate(num_products=Count('categories__product')).filter(num_products__gt=0)
      # Fetch the industries with the highest number of categories and brands
    top_industries = Industry.objects.annotate(
        num_categories=Count('categories'),
        num_brands=Count('categories__product__brand')
    ).order_by('-num_categories', '-num_brands')[:4]
    context = {
        "carts": carts,
        "sub_total": format(sub_total, ".2f"),
        "slider": slider,
        "industry": industry,
        "hot_products_in_cate": hot_products_in_cate,
        "trending_product": trending_product,
        "trending_division_title": trending_division_title,
        "popular_categories": popular_categories,
        "new_arrivals": new_arrivals,
        "customer_reviews": customer_reviews,
        "flash_sales": flash_sales,
        "featured_categories": featured_categories,
        "blog_highlights": blog_highlights,
        "newsletter_signup": newsletter_signup,
        "top_industries": top_industries,
    }
    return render(request, "home/home.html", context)

def newsletter_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Save the email to the NewsletterSignup model
            NewsletterSignup.objects.create(email=email)
            return HttpResponse('Thank you for signing up!')
    return redirect('home') 

def display_categories_post(request, id):
    query = request.GET.get('q', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    selected_brands = request.GET.getlist('brand')
    selected_attributes = request.GET.getlist('attribute')
    selected_vendors = request.GET.getlist('vendor')
    selected_subcategories = request.GET.getlist('subcategory')

    # Fetch the selected category
    category = Categories.objects.get(id=id)

    # Fetch products related to the selected category
    products = Product.objects.filter(categories=category)

    # Fetch related attributes and attribute values
    attributes = Attribute.objects.filter(product__categories=category).distinct()
    attribute_values = AttributeValue.objects.filter(attribute__product__categories=category).distinct()

    # Fetch related brands, vendors, product types, and subcategories
    brands = ProductBrand.objects.filter(product__categories=category).distinct()
    vendors = VendorStore.objects.filter(product__categories=category).distinct()
    product_types = ProductType.objects.filter(product__categories=category).distinct()
    subcategories = SubCategories.objects.filter(categories=category).distinct()

    # Apply filters
    if query:
        products = products.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if min_price:
        products = products.filter(regular_price__gte=min_price)
    if max_price:
        products = products.filter(regular_price__lte=max_price)
    if selected_brands:
        products = products.filter(brand_id__in=selected_brands)
    if selected_attributes:
        products = products.filter(attributes__in=selected_attributes).distinct()
    if selected_vendors:
        products = products.filter(vendor_stores_id__in=selected_vendors)
    if selected_subcategories:
        products = products.filter(subcategories_id__in=selected_subcategories)

    # Implement pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'products': products,
        'brands': brands,
        'vendors': vendors,
        'attributes': attributes,
        'attribute_values': attribute_values,
        'product_types': product_types,
        'subcategories': subcategories,
        'selected_brands': selected_brands,
        'selected_attributes': selected_attributes,
        'selected_vendors': selected_vendors,
        'selected_subcategories': selected_subcategories,
    }

    return render(request, "categories-post.html", context)



def test_page(request):
    return render(request, "strip/checkout.html")

def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 1400

# @csrf_exempt
# def create_checkout_session(request):
#     if request.method == 'POST':          
#         try:
#             data = json.loads(request.POST)
#             # Create a PaymentIntent with the order amount and currency
#             intent = stripe.PaymentIntent.create(
#                 amount=calculate_order_amount(data['items']),
#                 currency='usd',
#                 # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
#                 automatic_payment_methods={
#                     'enabled': True,
#                 },
#             )
#             return JsonResponse({
#                 'clientSecret': intent['client_secret']
#             })
            
#         except Exception as e:
#             return JsonResponse(error=str(e)), 403



