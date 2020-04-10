from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):    
    
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None 
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter Your Unique Username'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter Your Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Re-Enter Your Password'})
    class Meta:
        model = User
        fields = ['username','password1','password2']


