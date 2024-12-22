from django import forms
from products.models import PlacedOder, CustomerAddress


class PlacedOderForm(forms.ModelForm):

    class Meta:
        model = PlacedOder
        fields = ['order_number','sub_total_price', 'paid', 'status']
        widgets = {
        'sub_total_price': forms.NumberInput(attrs={'class': 'form-control','readonly': 'readonly'}),
        'status': forms.Select(attrs={'class': 'form-control'}),
        # 'shipping_address': forms.Select(attrs={'class': 'form-control','readonly': 'readonly'}),
        'paid': forms.CheckboxInput(attrs={'class': ''}),
        'order_number': forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}),
    }
        
    
# In forms.py
# forms.py
from django import forms
from products.models import Product, ProductImage
# forms.py
from django import forms
from products.models import Product, Categories, ProductBrand , Industry ,ProductType ,Attribute , AttributeValue
from Vendors.models import VendorStore
from ckeditor.widgets import CKEditorWidget



class ProductForm(forms.ModelForm):
    description = CKEditorWidget()
    details_description = CKEditorWidget()
    
    industry = forms.ModelChoiceField(
        queryset=Industry.objects.all(), 
        required=True,
        empty_label="Select Industry"
    )
    product_type = forms.ModelChoiceField(
        queryset=ProductType.objects.none(),  # Dynamically populated based on industry
        required=True,
        empty_label="Select Product Type"
    )
    attributes = forms.ModelMultipleChoiceField(
        queryset=Attribute.objects.none(),  # Dynamically populated based on product type
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    attribute_values = forms.ModelMultipleChoiceField(
        queryset=AttributeValue.objects.none(),  # Dynamically populated based on attributes
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Product
        fields = ['industry', 'product_type', 'title', 'regular_price', 'stoc', 'out_of_stoc', 
                  'discounted_parcent', 'description', 'modle', 'categories', 
                  'vendor_stores', 'details_description', 'brand', 'attributes', 'attribute_values']

        widgets = {
            'regular_price': forms.NumberInput(attrs={'min': 0}),
            'stoc': forms.NumberInput(attrs={'min': 0}),
            'discounted_parcent': forms.NumberInput(attrs={'min': 0, 'max': 100}),
            'categories': forms.Select(),
            'vendor_stores': forms.Select(),
            'brand': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs['instance']
            if instance.industry:
                self.fields['product_type'].queryset = ProductType.objects.filter(industry=instance.industry)
            if instance.product_type:
                self.fields['attributes'].queryset = Attribute.objects.filter(product_type=instance.product_type)
                self.fields['attribute_values'].queryset = AttributeValue.objects.filter(attribute__in=self.fields['attributes'].queryset)

        # Populate with all product types for initial form rendering
        self.fields['product_type'].queryset = ProductType.objects.all()

    class Media:
        js = ('js/dynamic_product_form.js',)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['name', 'industry']
        
        
class AttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = ['name', 'product_type']        
        
class AttributeValueForm(forms.ModelForm):
    class Meta:
        model = AttributeValue
        fields = ['value']        