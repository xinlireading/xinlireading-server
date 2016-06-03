from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm

class XLRRegistrationForm(ModelForm):

    # username = forms.EmailField(label='username', max_length=100)
    # password = forms.CharField(label='password', max_length=100)

    def __init__(self, *args, **kwargs):
        super(XLRRegistrationForm, self).__init__(*args, **kwargs)

    error_messages = {
        'duplicate_username': '此邮箱已经注册，你可以直接使用此邮箱登陆'
    }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username = username).exists():
            raise forms.ValidationError(
                self.error_messages['duplicate_username'], code='duplicate_username'
            )
        else:
            return username


    class Meta:
        model = User
        fields = ('username','password')

    def save(self, commit=True):
        # user = super(SignupForm, self).save(commit=False)
        # user.username = self.cleaned_data['username']
        # user.email = self.cleaned_data['username']
        # user.set_password(self.cleaned_data['password'])
        user = User.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class XLRAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='username', max_length=100)
    password = forms.CharField(label='password', max_length=100)
