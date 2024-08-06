# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
         
    path('', Home,name='home'),

    path('about/',About ,name='about'),

    path('furniture/',furniture ,name='furniture'),

    path('shop/',shop ,name='shop'),

    path('store/',Store,name='Store'),

    path('signup/', ClientSignupView.as_view(), name='client_signup'),

    path('login/', LoginPageView.as_view(), name='login_page'),
    
    
    path('logout/', logout_view, name='logout'),

     path('preferences/', edit_preferences, name='edit_preferences'),


    path('password_reset/', auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
             email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'),
             name='password_reset'),


    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html'),
             name='password_reset_done'),


    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html'),
             name='password_reset_confirm'),


    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'),
             name='password_reset_complete'),

        

        
]
