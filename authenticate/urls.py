from django.urls import path
from . import views



urlpatterns = [
    path('', views.homepage, name='home'), # home view
    path('log-in/', views.log_in, name='log_in'), # login form
    path('sign-up/', views.sign_up, name='sign_up'), # sign up form
    path('submit_signin', views.submit_signin, name='submit_signin'), # checking data for login
    path('submit_signup', views.submit_signup, name='submit_signup'), # checking data for sign up
    path('allowed', views.allowed, name='allowed'), # view for succes in making a profile
    path('protected', views.protected, name='protected'), # view that is allowed only for authorized users  
    path('logout/', views.logout_view, name='logout'),  # end a session
    path('setup_2fa/', views.setup_2fa, name='setup_2fa'),  # view for verifying code
    path('verify_2fa/', views.verify_2fa, name='verify_2fa') # checking verification code
]