from  django import forms
from .models import UserProfile
from django.contrib.auth.models import User


class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BootstrapModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class UserForm(BootstrapModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Your password does not match")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password',]


class UserProfileForm(BootstrapModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'image']


class UserFormWithoutPassword(BootstrapModelForm):
    username = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class PasswordForm(BootstrapModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        # clean the data
        cleaned_data = super(PasswordForm, self).clean()

        # check that the old password is correct
        old_password = cleaned_data.get('old_password')

        # check that the passwords match
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            raise forms.ValidationError("Your password does not match")

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'confirm_password', ]