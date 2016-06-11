from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm, Textarea, Form
from .models import UserProfile, TestStudent


# class TestStudentForm(forms.Form):
#     name = forms.CharField(label='your name', max_length=100)
class TestStudentForm(ModelForm):
    # gender = forms.CharField()
    class Meta:
        model = TestStudent
        fields = ['name', 'gender']
        # widgets = {
        #     'name': Textarea()
        # }

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
        # user.is_activated = False
        if commit:
            user.save()
            user_profile = UserProfile.objects.create(user=user, is_activated=False)
            user_profile.save()
        return user


class XLRAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='username', max_length=100)
    password = forms.CharField(label='password', max_length=100)

UNKNOWN = 'U'
MALE = 'M'
FEMALE = 'F'
GENDER_CHOICES = (
    (UNKNOWN, '请选择你的性别'),
    (MALE, '男'),
    (FEMALE, '女'),
)
YEAR_CHOICES = (
    [(-1, '年')] + [(i, str(i)) for i in range(2016, 1900, -1)]
)
MONTH_CHOICES = (
    [(-1, '月')] + [(i, str(i)) for i in range(1, 13)]
)
DAY_CHOICES = (
    [(-1, '日')] + [(i, str(i)) for i in range(1, 32)]
)
class EditProfileForm(Form):


    name = forms.CharField(max_length=100)
    address_country = forms.CharField(max_length=100)
    address_city = forms.CharField(max_length=100)

    birth_year = forms.ChoiceField(choices=YEAR_CHOICES)
    birth_month = forms.ChoiceField(choices=MONTH_CHOICES)
    birth_day = forms.ChoiceField(choices=DAY_CHOICES)

    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    intro = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows':4, 'cols':15}))

    # class Meta:
    #     model = UserProfile
    #     fields = ['name', 'gender']
    #
    # def save(self):
    #
    # def is_valid(self):
