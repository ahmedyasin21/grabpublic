from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import UserProfile
from django import forms


class UserUpdateForm(forms.ModelForm):

    
    class Meta:
        model = UserProfile
        fields = ["avatar",'displayname','background','background_2','background_3','background_4','background_5','bio']


    # def clean_email_address(self):
    #     email_address = self.cleaned_data["email_address"]
    #     if UserProfile.objects.filter(email_address__iexact=email_address).exists():
    #         raise forms.ValidationError("Email is invalid")
    #     return email_address


class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ["avatar",]