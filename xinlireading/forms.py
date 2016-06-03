from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm


class CustomUserCreationForm(UserCreationForm):
    # error_messages = {
    #     'duplicate_username': '此邮箱已经注册，你可以直接登陆',
    #     'required_username': '邮箱不能为空',
    #     'invalid_username': '请输入有效的邮箱地址',
    # }
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # self.fields.pop('password2')
        # del self.fields['password1']
        # del self.fields['password2']
        # self.fields['password1'].required = False
        # self.fields['password2'].required = False
        # self.fields['username'].error_messages = {
        #     'required': self.error_messages['required_username'],
        #     'invalid': self.error_messages['invalid_username'],
        #     'unique': self.error_messages['duplicate_username']
        # }
        
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data['username']
        if commit:
            user.save()
        return user


class XLRAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='username', max_length=100)
    password = forms.CharField(label='password', max_length=100)
