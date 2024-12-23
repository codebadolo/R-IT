from products.models import (PlacedOder, 
                             PlacedeOderItem, 
                             CustomerAddress,
                             CompletedOder,
                             CompletedOderItems,
                             Cart)
from accounts.models import CustomUser
from . forms import PlacedOderForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
import json
from django.views import View
from django.http import HttpResponse
from products.models import  (Product, ProductImage , Attribute,
                              ProductBrand ,ProductType , 
                              ProductTypeAttribute  , Categories ,
                              SubCategories ,AttributeValue,  Industry )
#from vendors.models import VendorStore, Categories
from django.http import JsonResponse
from .forms import AttributeForm , ProductTypeForm
from .forms import ProductForm ,CategoryForm  # You'll need to create a ProductForm
from django.shortcuts import render, redirect, get_object_or_404


@login_required(login_url='user_login')
def dashboard(request):
    customer_with_product_in_cart = CustomUser.objects.filter(customer_with_product_in_cart__isnull=False).distinct()
    total_placed_oder = PlacedOder.objects.all().__len__()
    total_completed_oder = CompletedOder.objects.all().__len__
    last_30_days = datetime.now() - timedelta(days=30)
    completed_oder_last_30_days = CompletedOder.objects.filter(complete_date__gte=last_30_days).count()
    context={
        "customer_with_product_in_cart":customer_with_product_in_cart,
        'total_placed_oder':total_placed_oder,
        "total_completed_oder":total_completed_oder,
        'completed_oder_last_30_days':completed_oder_last_30_days
    }
    return render(request,'admin-panel/dashboard.html', context)


@login_required(login_url='user_login')
def show_placed_oder_list(request):
    placed_oder_list = PlacedOder.objects.all()

    context={
        'placed_oder_list':placed_oder_list
    }

    return render(request, 'admin-panel/placed-oder-list.html', context)


@login_required(login_url='user_login')
def show_placed_oder_item_list(request, id):
    #getting the placed oder object by Id
    placed_oder = PlacedOder.objects.get(id=id)
    if request.method == 'POST':
        placed_oder_form = PlacedOderForm(request.POST, instance=placed_oder)
        if placed_oder_form.is_valid():
            placed_oder_form.save()
            messages.info(request, "Updated successfully")
    placed_oder_form = PlacedOderForm(instance=placed_oder)
    oder_item_list = PlacedeOderItem.objects.filter(placed_oder=placed_oder)

    if hasattr(placed_oder, 'redirect_adter_completion'):
        placed_oder.delete()
        return redirect('show_placed_oder_list')
    
    context ={
        "oder_item_list":oder_item_list,
        'placed_oder':placed_oder,
        'placed_oder_form':placed_oder_form,
        'order_number': placed_oder.order_number
    }

    return render(request,'admin-panel/placed-oder-item-details.html', context)

@login_required(login_url='user_login')
def show_completed_oder_list(request):
    completed_oder_list = CompletedOder.objects.all()

    context={
        'completed_oder_list':completed_oder_list
    }

    return render(request, 'admin-panel/completed_oder_list.html', context)

@login_required(login_url='user_login')
def show_completed_oder_item_list(request, id):
    #getting the placed oder object by Id
    completed_oder = CompletedOder.objects.get(id=id)
    # if request.method == 'POST':
    #     placed_oder_form = PlacedOderForm(request.POST, instance=completed_oder)
    #     if placed_oder_form.is_valid():
    #         placed_oder_form.save()
    #         messages.info(request, "Updated successfully")
    # placed_oder_form = PlacedOderForm(instance=completed_oder)
    oder_item_list = CompletedOderItems.objects.filter(completed_oder=completed_oder)   
    context ={
        "oder_item_list":oder_item_list,
        'completed_oder':completed_oder,
        'order_number': completed_oder.oder_number
    }

    return render(request,'admin-panel/completed-oder-item-details.html', context)

# View to list all products
@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'admin-panel/product_list.html', {'products': products})

@login_required
def add_product(request):
    # Only admin or relevant roles can access the add product page
    if not request.user.is_superuser:  # You can modify this check for specific roles
        return redirect('dashboard')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            # Add any additional logic you need here before saving, e.g., setting a vendor store, etc.
            product.save()
            return redirect('product_list')  # Redirect to a page where products are listed
    else:
        form = ProductForm()

    return render(request, 'admin-panel/add_product.html', {'form': form})
def view_products(request):
    # Logic for viewing the list of products
    return render(request, 'admin-panel/view_products.html')

def add_brand(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        brand_name = data.get('brand')
        brand = ProductBrand.objects.create(name=brand_name)
        return JsonResponse({'success': True, 'brand_id': brand.id})

def add_product_type(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_type_name = data.get('product_type')
        product_type = ProductType.objects.create(name=product_type_name)
        return JsonResponse({'success': True, 'product_type_id': product_type.id})

def get_attributes(request, product_type_id):
    product_type = ProductType.objects.get(id=product_type_id)
    attributes = product_type.attributes.all()
    attributes_data = [{'id': attr.id, 'name': attr.name} for attr in attributes]
    return JsonResponse({'attributes': attributes_data})
# views.py
# 
def add_category(request):
    if request.method == 'POST':
        # Logic to handle form submission and saving a category
        pass
    
    # Get the top-level categories
    categories = Categories.objects.all()
    return render(request, 'admin-panel/add-category.html', {'categories': categories})

def get_subcategories(request, category_id):
    # Fetch the subcategories for the selected category
    subcategories = SubCategories.objects.filter(categories_id=category_id)
    subcategories_list = [{'id': sub.id, 'name': sub.name} for sub in subcategories]
    return JsonResponse(subcategories_list, safe=False)

def category_list(request):
    categories = Categories.objects.all()
    return render(request, 'admin-panel/category-list.html', {'categories': categories})

from django.forms import inlineformset_factory
def edit_category(request, category_id):
    category = get_object_or_404(Categories, id=category_id)

    SubCategoryFormSet = inlineformset_factory(
        Categories,
        SubCategories,
        fields=('name',),
        extra=1,  # Allow adding one empty subcategory initially
        can_delete=True  # Allow deleting subcategories
    )

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        formset = SubCategoryFormSet(request.POST, instance=category)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
        formset = SubCategoryFormSet(instance=category)

    return render(request, 'admin-panel/edit-category.html', {
        'form': form,
        'formset': formset,
        'category': category
    })

def delete_category(request, category_id):
    category = get_object_or_404(Categories, id=category_id)
    category.delete()
    return redirect('category_list')

@login_required
def manage_attributes(request):
    if request.method == 'POST':
        form = AttributeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_attributes')
    else:
        form = AttributeForm()

    attributes = Attribute.objects.all()
    return render(request, 'admin-panel/manage_attributes.html', {'form': form, 'attributes': attributes})


from .forms import AttributeValueForm

@login_required
def manage_attribute_values(request, attribute_id):
    attribute = get_object_or_404(Attribute, id=attribute_id)
    
    if request.method == 'POST':
        form = AttributeValueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_attribute_values', attribute_id=attribute.id)
    else:
        form = AttributeValueForm(initial={'attribute': attribute})
    
    attribute_values = AttributeValue.objects.filter(attribute=attribute)
    return render(request, 'admin-panel/manage_attribute_values.html', {'form': form, 'attribute': attribute, 'attribute_values': attribute_values})

class DynamicProductCreateView(View):
    template_name = 'admin-panel/add_product.html'

    def get(self, request):
        form = ProductForm()
        industries = Industry.objects.all()
        return render(request, self.template_name, {
            'form': form,
            'industries': industries
        })

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            form.save_m2m()  # Save ManyToMany fields (attributes)
            return JsonResponse({'success': True, 'message': 'Product created successfully'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

# AJAX Views for dynamic loading

def load_product_types(request):
    industry_id = request.GET.get('industry_id')
    product_types = ProductType.objects.filter(categories__industry_id=industry_id).distinct()
    return JsonResponse(list(product_types.values('id', 'name')), safe=False)


def load_attributes(request):
    product_type_id = request.GET.get('product_type_id')
    attributes = Attribute.objects.filter(product_type_id=product_type_id)
    return JsonResponse(list(attributes.values('id', 'name')), safe=False)


def load_attribute_values(request):
    attribute_id = request.GET.get('attribute_id')
    values = AttributeValue.objects.filter(attribute_id=attribute_id)
    return JsonResponse(list(values.values('id', 'value')), safe=False)

def create_product_type(request):
    AttributeFormSet = inlineformset_factory(ProductType, Attribute, fields=('name',), extra=1)
    
    if request.method == "POST":
        form = ProductTypeForm(request.POST)
        formset = AttributeFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            product_type = form.save()
            attributes = formset.save(commit=False)
            for attribute in attributes:
                attribute.product_type = product_type
                attribute.save()
            # Stay on the same page after saving
            return render(request, 'admin-panel/product_type_form.html', {
                'form': ProductTypeForm(),
                'formset': AttributeFormSet(),
                'success': True
            })
    else:
        form = ProductTypeForm()
        formset = AttributeFormSet()

    return render(request, 'admin-panel/product_type_form.html', {
        'form': form,
        'formset': formset
    })
    
    
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        product_type_id = request.POST.get('product_type')
        
        if product_type_id:
            attributes = Attribute.objects.filter(product_type_id=product_type_id)
        
        if form.is_valid():
            product = form.save()
            # Save dynamic attributes and values here (if needed)
            return redirect('product_list')  # Redirect to product list or stay on the page
            
    else:
        form = ProductForm()
        attributes = None
    
    product_types = ProductType.objects.all()
    
    return render(request, 'admin-panel/add_product.html', {
        'form': form,
        'attributes': attributes,
        'product_types': product_types
    })    