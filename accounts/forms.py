from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import CustomUser

class RegistrationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'mobile', 'account_type', 'business_name', 'business_address', 'particular_info', 'password1', 'password2')

class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'mobile', 'account_type', 'business_name', 'business_address', 'particular_info']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'mobile', 'account_type', 'business_name', 'business_address', 'particular_info', 'password1', 'password2')
    
    account_type = forms.ChoiceField(
        choices=CustomUser.ACCOUNT_TYPE,
        widget=forms.RadioSelect,
        required=True,
        label="Account Type"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account_type'].widget.attrs.update({'id': 'id_account_type'})
        self.fields['business_name'].widget.attrs.update({'id': 'id_business_name'})
        self.fields['business_address'].widget.attrs.update({'id': 'id_business_address'})
        self.fields['particular_info'].widget.attrs.update({'id': 'id_particular_info'})