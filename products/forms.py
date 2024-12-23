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
        
        


class ProductFormAdmin(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'  # Include the relevant fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            category = self.instance.categories
            if category:
                self.fields['subcategories'].queryset = category.subcategories.all()
            else:
                self.fields['subcategories'].queryset = SubCategories.objects.none()
        else:
            self.fields['subcategories'].queryset = SubCategories.objects.none()
