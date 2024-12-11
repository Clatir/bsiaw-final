from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import PasswordResetForm
from captcha.fields import CaptchaField

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ten adres email jest już używany.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Dodajemy rolę do UserProfile
            role = self.cleaned_data['role']
            UserProfile.objects.create(user=user, role=role)
        return user
    
class EdytujUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name']

    

class CaptchaForm(forms.Form):
    captcha = CaptchaField(label="Udowodnij, że nie jesteś robotem")