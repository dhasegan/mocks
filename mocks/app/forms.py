from django import forms

# User manangement
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Password management
from django.contrib.auth.hashers import check_password

# App Models 
from models import *

# Datetime handler
import datetime

class RegisterForm(forms.Form):
    email = forms.CharField(
        label="Email Address",
        max_length=40,
        widget=forms.TextInput())
    name = forms.CharField(
        label="Name",
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
            if not str.isalpha(ch) and not ch == ' ' and not str.isdigit(ch):
                raise forms.ValidationError('Your name can only be made of characters a-z, A-Z, 0-9 or space.')
        if MUser.objects.filter(username__exact=name):
            raise forms.ValidationError("Your name is already taken.")
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if MUser.objects.filter(email__exact=email):
            raise forms.ValidationError("Email is already used.")
        for ch in email.encode('utf8'):
            if not str.isalpha(ch) and not str.isdigit(ch) and not ch == '.':
                raise forms.ValidationError('Your name can only be made of characters a-z, A-Z, 0-9 or dot(".")')
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

class CreateSlotForm(forms.Form):
    date = forms.DateField(
        label="When do you want to set up the mock interview? (MM/DD/YY)",
        required=True)
    time = forms.TimeField(
        label="At what time? Please input the time in Germany's timezone. (HH:MM)",
        required=True)

    def clean(self):
        date = self.cleaned_data.get('date')
        if type(date) != datetime.date:
            raise forms.ValidationError("""
                The date format you set is not correct. Please use one of those formats:
                '10/25/06',
                '10/25/2006' or
                '2006-10-25'
                """)
        time = self.cleaned_data.get('time')
        if type(time) != datetime.time:
            raise forms.ValidationError("""
                The time format you set is not correct. Please use one of those formats:
                '14:30' or
                '14:30:59'
                """)
        dt = datetime.datetime.combine(date, time)
        if dt < datetime.datetime.now():
            raise forms.ValidationError("""
                The date and time you set is in the past. Please insert a valid input.
                """)
        if dt > datetime.datetime.now() + datetime.timedelta(weeks=4):
            raise forms.ValidationError("""
                The date and time you set is in too far in the future. 
                Please insert a date that is not more that 1 month in the future.
                """)
        self.cleaned_data['datetime'] = dt
        return self.cleaned_data

class DeleteInterviewForm(forms.Form):
    description = forms.CharField(
        required=True,
        label="Why do you want to delete this mock interview?",
        max_length=400,
        widget=forms.Textarea(attrs={'class':'form-control'}))

class ProfileChangeForm(forms.Form):
    name = forms.CharField(
        required=True,
        label="Name",
        max_length=40,
        widget=forms.TextInput(attrs={'class':'form-control'}))
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

    def __init__(self, userid=None, *args, **kwargs):
        super(ProfileChangeForm, self).__init__(*args, **kwargs)
        self._userid = userid

    def clean(self):
        cleaned_data = super(ProfileChangeForm, self).clean()

        description = cleaned_data.get('description')
        if cleaned_data.get('isMocker') and (not description or len(description) == 0):
            raise forms.ValidationError("If you want to give mock interviews please provide a description about yourself")

        return cleaned_data

    def clean_name(self):
        name = self.cleaned_data.get('name')
        for ch in name.encode('utf8'):
            if not str.isalpha(ch) and not ch == ' ' and not str.isdigit(ch):
                raise forms.ValidationError('Your name can only be made of characters a-z, A-Z, 0-9 or space.')
        if MUser.objects.filter(username__exact=name).exclude(id = self._userid):
            raise forms.ValidationError("The name is already taken.")
        return name

class ProfileChangePasswordForm(forms.Form):
    oldpassword = forms.CharField(
        required=True,
        label="Old Password",
        max_length=40,
        widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password = forms.CharField(
        required=True,
        label="Password",
        max_length=40,
        widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirmPassword = forms.CharField(
        required=True,
        label="Confirm the Password",
        max_length=40,
        widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def __init__(self, user=None, *args, **kwargs):
        super(ProfileChangePasswordForm, self).__init__(*args, **kwargs)
        self._user = user

    def clean(self):
        cleaned_data = super(ProfileChangePasswordForm, self).clean()

        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirmPassword')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        return cleaned_data

    def clean_oldpassword(self):
        oldpassword = self.cleaned_data.get('oldpassword')

        if not check_password( oldpassword, self._user.password ):
            raise forms.ValidationError("The password is not correct!")

        return oldpassword