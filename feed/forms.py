from django import forms
from .models import Post, Comment

from django import forms

class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content', 'image')
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Напишите что-нибудь...',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'id': 'file-upload',
                'style': 'display: nine;'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(PostModelForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = ''
        self.fields['image'].label = ''

class CommentModelForm(forms.ModelForm):
    body = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Add a comment',
            'class': 'form-comment'
        })
    )
    
    class Meta:
        model = Comment
        fields = ('body', )