from django import forms
from .models import CustomerAddress , Product , SubCategories


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
        
        


'''class ProductFormAdmin(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'  # Include the relevant fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            category = self.instance.categories
            if 'subcategories' in self.fields:
                if category and hasattr(category, 'subcategories'):
                    self.fields['subcategories'].queryset = category.subcategories.all()
                else:
                    self.fields['subcategories'].queryset = SubCategories.objects.none()
            else:
                self.fields['subcategories'] = forms.ModelChoiceField(
                    queryset=SubCategories.objects.none(),
                    required=False,
                    label="Subcategory"
                )
'''
from django import forms
from .models import AttributeValue, Product ,Attribute

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


class ProductFormAdmin(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__' # Adjust fields as needed


    def __init__(self, *args, **kwargs):
        super(ProductFormAdmin, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['subcategories'].queryset = SubCategories.objects.filter(categories=self.instance.categories)
        else:
            self.fields['subcategories'].queryset = SubCategories.objects.none()
    '''    subcategories = forms.ModelChoiceField(
        queryset=SubCategories.objects.none(),
        required=False
    )'''


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