from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model  = Address
        fields = '__all__'
        exclude = ['billing_profile','address_type']
        widgets = {
        # 'billing_profile':forms.Select(attrs={'class':'form-control'}),
        'address_line_1':forms.TextInput(attrs={'class':'form-control'}),
        'address_line_2':forms.TextInput(attrs={'class':'form-control'}),
        'city':forms.TextInput(attrs={'class':'form-control'}),
        'state':forms.TextInput(attrs={'class':'form-control'}),
        'postal_code':forms.TextInput(attrs={'class':'form-control'}),
        'country':forms.TextInput(attrs={'class':'form-control'}),
        'phone_no':forms.TextInput(attrs={'class':'form-control'}),
        }
