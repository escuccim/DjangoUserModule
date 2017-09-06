from  django import forms
from .models import UserProfile
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BootstrapModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class BootstrapForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BootstrapForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class UserForm(BootstrapModelForm):
    username = forms.CharField(label=_("Username"))
    email = forms.EmailField(label=_("Email"))
    password = forms.CharField(widget=forms.PasswordInput(),label=_("Password"))
    confirm_password = forms.CharField(widget=forms.PasswordInput(),label=_("Confirm Password"))
    first_name = forms.CharField(required=False,label=_("First name"))
    last_name = forms.CharField(required=False,label=_("Last name"))

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            msg = _("Your passwords do not match")
            self.add_error('new_password', msg)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password','first_name', 'last_name']


class UserProfileForm(BootstrapModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ['image']


class UserFormWithoutPassword(BootstrapModelForm):
    username = forms.CharField(label=_("Username"))
    email = forms.EmailField(label=_("Email"))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class PasswordForm(BootstrapModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput(),label=_("Old Password"))
    new_password = forms.CharField(widget=forms.PasswordInput(),label=_("New Password"))
    confirm_password = forms.CharField(widget=forms.PasswordInput(),label=_("Confirm Password"))

    def clean(self):
        # clean the data
        cleaned_data = super(PasswordForm, self).clean()

        # check that the passwords match
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            msg = _("Your passwords do not match")
            self.add_error('new_password', msg)

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'confirm_password', ]


class PasswordResetForm(BootstrapForm):
    email = forms.EmailField(label=_("Email"))

    class Meta:
        fields = ['email',]


class ChangePasswordForm(BootstrapModelForm):
    password = forms.CharField(widget=forms.PasswordInput(),label=_("Password"))
    confirm_password = forms.CharField(widget=forms.PasswordInput(),label=_("Confirm password"))

    # check that the passwords match
    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()

        # check that the passwords match
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # if not add an error
        if password != confirm_password:
            msg = _("Your passwords do not match")
            self.add_error('password', msg)

    class Meta:
        model = User
        fields = ['password', 'confirm_password']