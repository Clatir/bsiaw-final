from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django_otp.plugins.otp_totp.models import TOTPDevice
from .models import UserProfile
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from .decorators import role_required
from django import forms
import qrcode
import io, base64
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from .forms import CaptchaForm

class OTPVerificationForm(forms.Form):
    otp_token = forms.CharField(label="Kod OTP", max_length=6)

def register(request):
    """Widok rejestracji użytkownika."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Automatyczne logowanie po rejestracji
            return redirect('role_redirect')  # Przekierowanie na odpowiednią stronę
    else:
        form = UserRegistrationForm()
    return render(request, 'authentication/register.html', {'form': form})

#def log_in(request):
#    if request.method == 'POST':
#        form = AuthenticationForm(data=request.POST)
#        if form.is_valid():
#            user = form.get_user()
#            login(request, user)
#            return redirect('role_redirect')
#    else:
#        form = AuthenticationForm()
#    return render(request, 'authentication/login.html', {'form': form}) 

def log_in(request):
    """Proces logowania z obsługą OTP."""
    #form = None
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            #user = form.get_user()
            user = authenticate(request=request, username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            profile = UserProfile.objects.select_related('user').get(user=user)
            if profile.otp_enabled == True:
                # Jeśli OTP jest włączone, przejdź do drugiego kroku
                request.session['pre_authenticated_user_id'] = user.id
                return redirect('otp_verify')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('role_redirect')
    else:
        #form = AuthenticationForm()
        form = AuthenticationForm(request=request, data=request.POST if request.method == 'POST' else None)
    return render(request, 'authentication/login.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('login')      

@login_required
def role_based_redirect(request):
    """Przekierowanie użytkownika na stronę odpowiednią dla jego roli."""
    profile = UserProfile.objects.get(user=request.user)
    if profile.role == 'ref':
        return redirect('judge_dashboard')
    elif profile.role == 'kol':
        return redirect('committee_dashboard')
    return redirect('undefined_dashboard')


@login_required
def enable_otp(request):
    """Widok włączania OTP dla użytkownika."""
    profile = UserProfile.objects.get(user=request.user)
    if not profile.otp_enabled:
        device = TOTPDevice.objects.create(user=request.user, confirmed=True)
        profile.otp_enabled = True
        profile.save()
        qr_code_url = device.config_url

        qr = qrcode.make(qr_code_url)
        
        # Konwersja QR do obrazu w pamięci
        #buffer = io.BytesIO()
        #qr.save(buffer, format="PNG")
        #buffer.seek(0)
        #qr_code_data = buffer.getvalue()
        buffer = io.BytesIO()
        qr.save(buffer, format="PNG")
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()


        return render(request, 'authentication/enable_otp.html', {
            'qr_code_url': qr_code_url,
            'qr_code_data': qr_code_base64,
        })
    return redirect('role_redirect')


@login_required
@role_required('ref')
def judge_dashboard(request):
    """Strona główna dla roli 'Sędzia'."""
    return render(request, 'authentication/referee.html', {'profile': request.user.userprofile})


@login_required
@role_required('kol')
def committee_dashboard(request):
    """Strona główna dla roli 'Kolegium'."""
    return render(request, 'authentication/kolegium.html', {'profile': request.user.userprofile})



def otp_verify(request):
    """Widok do weryfikacji OTP."""
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('pre_authenticated_user_id')
            if user_id:
                user = User.objects.get(id=user_id)
                device = TOTPDevice.objects.filter(user=user).first()
                if device and device.verify_token(form.cleaned_data['otp_token']):
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    del request.session['pre_authenticated_user_id']
                    return redirect('role_redirect')
        return render(request, 'authentication/otp_verify.html', {'form': form, 'error': 'Nieprawidłowy kod OTP'})
    else:
        form = OTPVerificationForm()
    return render(request, 'authentication/otp_verify.html', {'form': form})

@login_required
def manage_otp(request):
    """Widok umożliwiający zarządzanie OTP (włączanie/wyłączanie)."""
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        if 'enable_otp' in request.POST and not profile.otp_enabled:
            # Włączanie OTP
            device = TOTPDevice.objects.create(user=request.user, confirmed=True)
            profile.otp_enabled = True
            profile.save()
            return render(request, 'authentication/enable_otp.html', {'qr_code_url': device.config_url})
        elif 'disable_otp' in request.POST and profile.otp_enabled:
            # Wyłączanie OTP
            TOTPDevice.objects.filter(user=request.user).delete()
            profile.otp_enabled = False
            profile.save()
            return redirect('role_redirect')
    return render(request, 'authentication/manage_otp.html', {'profile': profile})

@login_required
class CustomPasswordResetView(PasswordResetView):
    
    
    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            # Sprawdzenie OTP
            profile = UserProfile.objects.select_related('user').get(user=user)
            if profile.otp_enabled:
                otp_token = self.request.POST.get('otp_token')
                device = TOTPDevice.objects.filter(user=user).first()
                if not device or not device.verify_token(otp_token):
                    messages.error(self.request, "Nieprawidłowy kod OTP.")
                    return self.form_invalid(form)
            return super().form_valid(form)
        except User.DoesNotExist:
            # Udajemy sukces (nie zdradzamy, że email nie istnieje)
            return super().form_valid(form)
        

#def CaptchaValidationView(request):
#    if request.method == 'POST':
#        form = CaptchaForm(request.POST)
#        if form.is_valid():
#           # CAPTCHA rozwiązana poprawnie, przekieruj do strony resetu hasła
#            return redirect('password_reset')
#        return render(request, 'authentication/captcha_validation.html', {'form': form, 'error': 'Niepoprawna CAPTCHA. Spróbuj ponownie.'})
#    form = CaptchaForm()
#    return render(request, 'authentication/captcha_validation.html', {'form': form})