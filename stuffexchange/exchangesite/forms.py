from django import forms
from django.forms import inlineformset_factory

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


class GoodForm(forms.ModelForm):

    class Meta:
        model = Good
        fields = ('category', 'title', 'description')


GalleryFormSet = inlineformset_factory(Good,
                                       Gallery,
                                       fields=('image',),
                                       extra=5,
                                       max_num=5,
                                       can_delete=False)

