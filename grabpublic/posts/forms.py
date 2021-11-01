from django import forms
from .models import Post,Comment
from django.core.exceptions import ValidationError




class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('tag',"title","image_data")

        widgets ={
            'title' : forms.Textarea(attrs={'class':'editable medium-editor-textarea postbody'}),
            'tag': forms.CheckboxSelectMultiple
        }

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = ''
        self.fields['image_data'].label = ''
        self.fields['title'].error_messages = {'required': 'Title is require'}
    

    def clean_image_data(self):
        img = self.cleaned_data["image_data"]
        print(img,'im im im im im mi')
        if not img:
              raise ValidationError(
                    "Did not send for 'help' in the subject despite "
                    "CC'ing yourself."
                )
        return img


    
        



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
    

    