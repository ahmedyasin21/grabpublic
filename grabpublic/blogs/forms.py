from django import forms
from .models import Blog,Comment
import re 




class BlogForm(forms.ModelForm):
    
    class Meta:
        model = Blog
        fields = ("title","image_data","body",'tag')

        widgets ={
            'title' : forms.TextInput(attrs={'class':'blogtitle','placeholder':'Title',}),
            'body':  forms.Textarea(attrs={'class':'editable medium-editor-textarea blogbody'}),
            'image_data': forms.FileInput(attrs={'class':'blogimage'}),
            'tag': forms.CheckboxSelectMultiple
        }

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].label = ''
        self.fields['title'].label = ''
        self.fields['image_data'].label = ''




class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('parent',"body",)
        widgets ={
            'body' : forms.TextInput(attrs={'class':'textinputclass','class':'form-control'}), 
        }

    
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['parent'].widget.attrs.update(
            {'class': 'd-none'})
        self.fields['parent'].label = ''
        self.fields['body'].widget.attrs['placeholder'] = ('Write new comment')
        self.fields['body'].label = ''
        self.fields['parent'].required = False