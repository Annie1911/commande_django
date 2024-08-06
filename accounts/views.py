# accounts/views.py
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LoginForm ,CustomUserCreationForm,UserPreferenceForm
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth import logout as auth_logout
from .models import User
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from .models import UserPreference

@login_required
def edit_preferences(request):
    user_pref, created = UserPreference.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserPreferenceForm(request.POST, instance=user_pref)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserPreferenceForm(instance=user_pref)
    return render(request, 'edit_preferences.html', {'form': form})


class ClientSignupView(View):
    form_class = CustomUserCreationForm
    template_name = 'client_signup.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            user.role = 'client'
            user.save()
            login(request, user)
            return redirect('login_page')
        return render(request, self.template_name, {'form': form})


def Home(request):
    return render(request,'home.html')

def furniture(request):
    return render(request,'furniture.html')

def shop(request):
    return render(request,'shop.html')

def About(request):
    return render(request,'about.html')

def Store(request):
    return render(request,'store.html')

def logout_view(request):
    auth_logout(request)
    return redirect('home')

@method_decorator(csrf_protect, name='dispatch')
class LoginPageView(View):
    template_name = 'login_page.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
        
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.role == 'responsable':
                    return redirect('commandes_reçu')
                elif user.role == 'caissier':
                    return redirect('recevoir_commandes')
                elif user.role == 'comptable':
                    return redirect('consulter_ventes')
                elif user.role == 'client':
                    if User.objects.filter(username=username).exists():
                        return redirect('index')
                    else:
                        return redirect('client_signup')
            error = 'Utilisateur inconnu.'
        else:
            error = 'Veuillez corriger les erreurs dans le formulaire.'
        
        return render(request, self.template_name, {'form': form, 'error': error})