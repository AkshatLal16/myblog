import os
from django import forms
from .models import *
from ckeditor_uploader.fields import RichTextUploadingField
from django.forms.widgets import ClearableFileInput
from openforums import settings

class AddStoryForm(forms.ModelForm):
    title = forms.CharField(
        label = 'Title',
        max_length =500,
        required = True,
        widget = forms.TextInput(
            attrs = {'class':'form-control1','placeholder':'Title'}
        )
    )
    category = forms.ModelChoiceField(
        queryset = Genre.objects.all(), 
    )
    class Meta:
        model = Story
        fields = ('title', 'body', 'category')

class ClearableFileInput1(ClearableFileInput):
    template_name = os.path.join(settings.BASE_DIR, 'users/templates/users/snippet/image-upload-button.html')

class EditProfileForm(forms.ModelForm):
    image = forms.ImageField(widget=ClearableFileInput1())
    class Meta:
        model = Profile
        fields = ['bio','image']

class AddResponseForm(forms.ModelForm):
    body = forms.CharField(
        label = 'Title',
        max_length =10000,
        required = True,
        widget = forms.Textarea(
            attrs = {'class':'form-control text-wrap','placeholder':'Write a response', 'rows':'2'}
        )
    )
    class Meta:
        model = Responses
        fields = ['body']

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['comment']