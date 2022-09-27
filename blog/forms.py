from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from blog.models import Post


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title_tag", "title", "body", "author", "category", "post_image"]

        widgets={
            "title_tag":forms.TextInput(attrs={"class":"form-content", "placeholder":"Title Tag"}),
            "title":forms.TextInput(attrs={"class":"form-content", "placeholder":"Title"}),
            "body": forms.TextInput(attrs={"class": "form-content"}),
            "author": forms.TextInput(attrs={"class": "form-content"}),
            "category": forms.TextInput(attrs={"class": "form-content"}),
        }

class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title_tag", "title", "body", "category", "post_image"]

        widgets={
            "title_tag":forms.TextInput(attrs={"class":"form-content", "placeholder":"Title Tag"}),
            "title":forms.TextInput(attrs={"class":"form-content", "placeholder":"Title"}),
            "body": forms.TextInput(attrs={"class": "form-content"}),
            "category": forms.TextInput(attrs={"class": "form-content"}),
        }

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]