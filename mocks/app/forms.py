from django import forms

from django.contrib.auth.models import User
from models import *
from django.contrib.auth import authenticate

class RegisterForm(forms.Form):
    email = forms.CharField(
        label="Email Address",
        max_length=40,
        widget=forms.TextInput())
    name = forms.CharField(
        label="Real Name",
        max_length=40,
        widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(
        label="Password",
        max_length=40,
        widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirmPassword = forms.CharField(
        label="Confirm the Password",
        max_length=40,
        widget=forms.PasswordInput(attrs={'class':'form-control'}))
    skypeId = forms.CharField(
        required=False,
        label="Skype Id",
        max_length=40,
        widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(
        required=False,
        label="For what companies you want to apply or companies that you applied for which you want to share your experience",
        max_length=400,
        widget=forms.Textarea(attrs={'class':'form-control'}))
    isMocker = forms.BooleanField(
        required=False,
        label="Do you want to give mock interviews to other students? If yes, please give a good description in the field above.")


    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirmPassword')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        description = cleaned_data.get('description')
        if cleaned_data.get('isMocker') and (not description or len(description) == 0):
            raise forms.ValidationError("If you want to give mock interviews please provide a description about yourself")

        return cleaned_data

    def clean_name(self):
        name = self.cleaned_data.get('name')
        for ch in name.encode('utf8'):
            if not str.isalpha(ch) and not ch == ' ':
                raise forms.ValidationError('Your name can only be made of characters a-z, A-Z or space.')
        if MUser.objects.filter(username__exact=name):
            raise forms.ValidationError("Your name is already taken.")
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if MUser.objects.filter(email__exact=email):
            raise forms.ValidationError("Email is already used.")
        return email

class LoginForm(forms.Form):
    email = forms.CharField(
        label="Email Address",
        max_length=40,
        widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(
        label="Password",
        max_length=40,
        widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()

        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        muser = MUser.objects.filter(email__exact=email)
        if len(muser) != 1:
            raise forms.ValidationError("Invalid email and/or password!")
        user = authenticate(username=muser[0].username, password=password)
        if user is None:
            raise forms.ValidationError("Invalid email and/or password!")
        if not user.is_active:
            raise forms.ValidationError("Your account may not be activated! Try checking your email!")
        return cleaned_data