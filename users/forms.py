from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import Profile

class RegistrationForm(UserCreationForm):
    
    # email = forms.EmailField(required=True)
    email = forms.EmailField() # doldurulması zorunlu olsun istiyorsak (default-> blank=True 'dur. Bu şekilde required=True olmuş oluyor.)

    class Meta:
        model = User
        fields = ('username', 'email') # password1 ve password2'yi belirtmeye gerek yok
    
    def clean_email(self):
        email = self.cleaned_data['email']  # user@gmail.com
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu e-posta adresi zaten kullanımda.')
        return email


class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('image', 'bio',)
        
        
class UserUpdateForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('username', 'email')
        

#! email-password ile login yapmak için form; 
from django.contrib.auth.forms import (
    AuthenticationForm,
)
from django.contrib.auth import authenticate

class EmailLoginForm(AuthenticationForm):

    username = forms.EmailField(label="Email")  # E-posta alanı kullan

    def clean(self):
        email = self.cleaned_data.get('username')  # Form'daki "username" alanını email olarak kabul ediyoruz
        password = self.cleaned_data.get('password')

        if email and password:
            try:
                # E-posta ile kullanıcıyı bul
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("Bu e-posta ile bir kullanıcı bulunamadı.")
            
            # Bulunan kullanıcının kullanıcı adını (username) authenticate'e gönderiyoruz
            self.user_cache = authenticate(self.request, username=user.username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Geçersiz e-posta veya şifre.")
        
        return self.cleaned_data

    def get_user(self):
        return self.user_cache


#! email-reset için email'in db'de olup olmadığının kontrolü; 
class PasswordResetEmailCheckForm(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu e-posta adresi ile kayıtlı bir hesap bulunamadı.')
        return email