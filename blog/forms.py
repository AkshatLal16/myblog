from django import forms
from users.models import *

class Login(forms.ModelForm):
	password = forms.CharField(max_length=100 , widget=forms.PasswordInput)
	class Meta:
		model = Profile
		fields = ['username','password']