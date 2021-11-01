from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import UserProfile
from django import forms


class UserUpdateForm(forms.ModelForm):

    
    class Meta:
        model = UserProfile
        fields = ["avatar",'displayname','background','background_2','background_3','background_4','background_5','bio']

        widgets ={
            
                # 'avatar': forms.ImageField(attrs={'class':'form-control'}, required=True),
                'displayname' : forms.TextInput(attrs={'class':'form-control'}),
                # 'last_name' : forms.TextInput(attrs={'class':'form-control'}),
                # 'age' : forms.TextInput(attrs={'class':'form-control','title':'Age should be more then 18'}),
                # 'gender' : forms.Select(choices=Gender,attrs={'class': 'form-control'}),
                # 'country': CountrySelectWidget(),
                # 'phone': PhoneNumberPrefixWidget(),
                # 'username' : forms.TextInput(attrs={'class': 'form-control','id':'disabledInput'}),
                # 'email' : forms.TextInput(attrs={'class': 'form-control','id':'eMail'}),
                'bio' : forms.TextInput(attrs={'class': 'form-control','id':'bio','rows':2, 'cols':15}),
        }

    # def clean_email_address(self):
    #     email_address = self.cleaned_data["email_address"]
    #     if UserProfile.objects.filter(email_address__iexact=email_address).exists():
    #         raise forms.ValidationError("Email is invalid")
    #     return email_address


class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ["avatar",]