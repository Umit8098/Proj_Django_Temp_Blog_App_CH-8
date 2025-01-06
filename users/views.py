from django.shortcuts import render, redirect
from .forms import (
    RegistrationForm,
    ProfileUpdateForm,
    UserUpdateForm,
)
from django.contrib import messages


def register(request):
    
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in!")
        return redirect('blog:list')  #! Kullanıcı zaten giriş yapmışsa yönlendirilecek sayfa. Bir kullanıcının mükerrer kaydını engellemek için bu kontrolü yapabiliriz.
    
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        form.save()
        # name = form.cleaned_data.get('username')
        name = form.cleaned_data['username']
        messages.success(request, f"Account created for {name} successfully.")
        return redirect('login') # login page'imizi oluşturduk.
    
    context = {
        'form': form
    }
    return render(request, 'users/register.html', context)


def profile(request): 
    
    p_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user.profile)
    
    u_form = UserUpdateForm(request.POST or None, instance=request.user)
        
    if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()
        messages.success(request, "Your profile has been updated!")

        return redirect(request.path)
    
    context = {
        'p_form': p_form,
        'u_form': u_form,
    }
    return render(request, 'users/profile.html', context)


#! email-password ile login yapmak için views;
from .forms import EmailLoginForm
from django.contrib.auth import login
from django.contrib import messages

def user_login(request):
    
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in!")
        return redirect('blog:list')  #! Kullanıcı zaten giriş yapmışsa yönlendirilecek sayfa

    form = EmailLoginForm()
    if request.method == 'POST':
        form = EmailLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('blog:list')
    context = {
        'form': form,
    }
    return render(request, 'users/user_login.html', context)

