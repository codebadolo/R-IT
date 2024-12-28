from django import forms
from .models import CustomerAddress , Product , SubCategories ,AttributeValue

from .models import AttributeValue, Product ,Attribute

class CustomerAddressForm(forms.ModelForm):
    class Meta:
        model = CustomerAddress
        fields = ['state','city','zip_code','street_address','mobile']
        widgets = {
            'state': forms.TextInput(attrs={'class':'form-control'}),
            'city': forms.TextInput(attrs={'class':'form-control'}),
            'zip_code': forms.NumberInput(attrs={'class':'form-control'}),
            'street_address': forms.Textarea(attrs={'class':'form-control','rows':5,'cols':50}),
            'mobile': forms.NumberInput(attrs={'class':'form-control'}),
        }   
        



class AttributeValueInlineForm(forms.ModelForm):
    class Meta:
        model = AttributeValue
        fields = ['attribute', 'value']

    def __init__(self, *args, **kwargs):
        super(AttributeValueInlineForm, self).__init__(*args, **kwargs)
        # Dynamically filter attributes based on selected product type
        if 'product' in self.data:
            try:
                product_id = int(self.data.get('product'))
                product = Product.objects.get(pk=product_id)
                self.fields['attribute'].queryset = Attribute.objects.filter(product_type=product.product_type)
            except (ValueError, TypeError):
                self.fields['attribute'].queryset = Attribute.objects.none()
        elif self.instance.pk:
            self.fields['attribute'].queryset = self.instance.product.product_type.attribute_set.all()


from django import forms
from .models import Product, SubCategories

class ProductFormAdmin(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title', 'slug', 'regular_price', 'stoc', 'out_of_stoc', 'discounted_parcent', 
            'description', 'modle', 'categories', 'subcategories', 'tag', 'vendor_stores', 
            'details_description', 'brand', 'product_type', 'inventory', 'attributes'
        ]  # Specify required fields

    def __init__(self, *args, **kwargs):
        super(ProductFormAdmin, self).__init__(*args, **kwargs)
        if 'categories' in self.data:
            try:
                category_id = int(self.data.get('categories'))
                self.fields['subcategories'].queryset = SubCategories.objects.filter(categories_id=category_id)
            except (ValueError, TypeError):
                self.fields['subcategories'].queryset = SubCategories.objects.none()
        elif self.instance.pk:
            self.fields['subcategories'].queryset = SubCategories.objects.filter(categories=self.instance.categories)
        else:
            self.fields['subcategories'].queryset = SubCategories.objects.none()

'''    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('categories'))
                self.fields['subcategories'].queryset = SubCategories.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategories'].queryset = SubCategories.objects.filter(categories=self.instance.categories)'''
'''    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Populate subcategories if editing an existing product
        if self.instance.pk and self.instance.categories:
            self.fields['subcategories'].queryset = self.instance.categories.subcategories.all()

        # Fallback for new products
        else:
            self.fields['subcategories'].queryset = SubCategories.objects.none()'''