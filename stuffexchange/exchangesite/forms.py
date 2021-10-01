from django import forms
from .models import CustomUser, Good, Gallery


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'communication_contact',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class AddGoodForm(forms.ModelForm):

    class Meta:
        model = Good
        fields = ('category', 'title', 'description')


class GalleryForm(forms.ModelForm):

    class Meta:
        model = Gallery
        fields = ('image',)

