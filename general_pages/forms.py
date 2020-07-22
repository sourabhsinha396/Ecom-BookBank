from django import forms
from .models import contactus


class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model  = contactus
        fields = '__all__'  #or do  ['name','email',etc]

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if "admin" in name:
            raise forms.ValidationError("Name cann't have the word Admin")
        return name
