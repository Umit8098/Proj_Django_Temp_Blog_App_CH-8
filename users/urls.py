from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    register,
    profile,
    user_login,
)
from .forms import PasswordResetEmailCheckForm

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(), name='login' ),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout' ),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    
    #! email-password ile login yapmak için path; 
    path('user_login/', user_login, name='user_login'),
    
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_email.html', form_class=PasswordResetEmailCheckForm), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='users/password_change_form.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
]
