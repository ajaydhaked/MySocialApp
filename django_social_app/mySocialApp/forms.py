from django import forms
from .models import Dweet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class Dweetform(forms.ModelForm):
    body = forms.CharField(required=True,
    widget=forms.widgets.Textarea(
        attrs={
            "placeholder": "Dweet something...",
            "class": "textarea is-success is-medium",
        }
    ),
    label="",                       
    )
    
    class Meta :
        model = Dweet
        exclude = ("user",)

class customUserCreationForm(UserCreationForm):
    email = forms.EmailField( required=False)
    class Meta:
        model = User
        fields=["username",'email',"password1",'password2']
    def save(self,commit=True):
        user = super(customUserCreationForm, self).save(commit=False)
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
        return user
