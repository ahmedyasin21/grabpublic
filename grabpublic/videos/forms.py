from django import forms
from .models import Video 

class VideoForm(forms.ModelForm):
    
    class Meta:
        model = Video
        fields = ("url",)

class SearchForm(forms.Form):

    search = forms.CharField(max_length=255, required=False)
    


