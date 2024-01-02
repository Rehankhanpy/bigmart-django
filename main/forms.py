from django import forms
from .models import Accounts

class RegistrationForm(forms.ModelForm):
       password = forms.CharField(widget=forms.PasswordInput(attrs={
              'placeholder':'Enter Password'
       }))
       confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
              'placeholder':'Confirm Password'
       }))
       class Meta:
              model = Accounts
              fields = ['firstname', 'lastname', 'phone_number', 'password', 'email']

       def clean(self):
              cleaned_data = super(RegistrationForm, self).clean()
              password = cleaned_data.get('password')
              confirm_password = cleaned_data.get('confirm_password')

              if password != confirm_password:
                     raise forms.ValidationError(
                            'Passwowrds Do Not Match'
                     )

       def __init__(self, *args, **kwargs):
              super(RegistrationForm, self).__init__(*args, **kwargs)
              self.fields['firstname'].widget.attrs['placeholder'] = 'Enter First Name'
              self.fields['lastname'].widget.attrs['placeholder'] = 'Enter Last Name'
              self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
              self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
              
              
              for field in self.fields:
                     self.fields[field].widget.attrs['class'] = 'form-control'

       
              