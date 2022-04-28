"""Importing Comment"""
from xml.etree.ElementTree import Comment
from django import forms
from .models import Comment
class EmailPostForm(forms.Form):
    """Emial post form class"""
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False,  widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    """Letting users fill the form"""
    class Meta:
        """Creating a comment"""
        model = Comment
        fields = ("name","email","body")

class SearchForm(forms.Form):
    """Creating the search form class"""
    query = forms.CharField()
