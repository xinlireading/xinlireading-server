from django import forms

class SigninForm(forms.Form):
    email = forms.CharField(label='email', max_length=100)
    password = forms.CharField(label='password', max_length=100)
    # print('email: ' + str(email))
    # print('password: ' + str(password))
