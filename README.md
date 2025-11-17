# authenticate
Setting up a Protected Area for a Django Website

# Introducion
This document provides instruction on how to set up a protected area in a Django website project.This is useful when you want to restrict access to certain parts of your webpage to authenticated users only. As an addition, it provides instrucions for creating a <strong>2 Factor Authentication</strong> using django_otp. Two-Factor Authentication (2FA) can be used for email verification. This adds an extra layer of security to your application by requiring users to verify their identity using a second factor, in this case, a verification code sent to their email. Django OTP is a Django app that provides an easy way to implement 2FA in your project. It supports various types of one-time password devices, such as email, SMS, QR code, and hardware tokens.

# Prerequisites
Before you begin, make sure you have the following:
<ul>
  <li>Python installed on your system.</li>
  <li>Django installed in your Python environment.</li>
  <li>A Django project set up and go.</li>
  <li>Basic understanding of Two-Factor Authentication</li>
</ul>

# Installation
To install Django OTP, run the following command in the terminal:
<code>pip install django-otp</code>

# Steps 
<ol>
<li><strong>Set Up Authentication:</strong> Django comes with a built-in user authentication system. You can use this to handle user registration, login, and logout. Follow the official Django documentation to set this up.</li>
<li><strong>Create a Login View:</strong> If you don't have one, create a view where users can log in. This can be a form that takes a username and password.</li>
<li><strong>Protect your views:</strong> In the views that you want to protect, use @login_required decorator. This will ensure that only logged in users can access the view.
  
  <code>from django.contrib.auth.decorators import login_required
@login_required
def my_protected_view(request):
    # code logic here</code>

As an alternative, you can manually check if the user is authenticated.

<code>def my_protected_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    # code logic here
</code>
<i>In this code <code>request.user.is_authenticated</code> will return <code>True</code> if the user is logged in and <code>False</code> otherwise. In that case, user is redirected to the login page.</i></li>
<li><strong>Update Your URLs:</strong>  In your <strong>urls.py</strong> file, make sure that Django knows where your login view is. You can do this by setting the <strong>LOGIN_URL</strong> setting.

<code>from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.login_view, name='login'),
    # Your other urls here
]</code></li>
<li><strong>Test:</strong> Test your protected area by trying to access the protected views. If you’re not logged in, Django should redirect you to the login page.</li>
</ol>

## As for 2FA implementation, follow these steps:
<ol>
  <li>Make sure you have the following installed in your projects <code>settings.py</code> file: 

<code>INSTALLED_APPS = [
    ...
    'django_otp',
    'django_otp.plugins.otp_totp',
    ]</code>
  </li>

Remember to run migrations after installation using
<code>python manage.py makemigrations</code>
  and
  <code>python manage.py migrate</code>
  
  <li>Implement Django settings for sending emails (in this case) using SMTP (Simple Mail Transfer Protocol) with Gmail as the email service provider. It will look something like this:

<code>EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your@email.com'
EMAIL_HOST_PASSWORD = 'yourEmailPassword'
EMAIL_USE_SSL = False</code></li>

<i>Note: You should have allowed firewall for PORT 587</i>
</li>

<li>Last but not least:
  
## Don't forget to add necessarily paths in your url patterns:
<code>urlpatterns = [
    path('', views.homepage, name='home'), # home view
    path('log-in/', views.log_in, name='log_in'), # login form
    path('sign-up/', views.sign_up, name='sign_up'), # sign up form
    path('submit_signin', views.submit_signin, name='submit_signin'), # checking data for login
    path('submit_signup', views.submit_signup, name='submit_signup'), # checking data for sign up
    path('allowed', views.allowed, name='allowed'), # view for succes in making a profile
    path('protected', views.protected, name='protected'), # view that is allowed only for authorized users  
    path('logout/', views.logout_view, name='logout'),  # end a session
    path('setup_2fa/', views.setup_2fa, name='setup_2fa'),  # view for verifying code
    path('verify_2fa/', views.verify_2fa, name='verify_2fa') # checking verification code]</code></li></ol>

## As for views.py file, you should know the following:
### User Registration and Login

The project includes the following views and functions for user registration and login:

- `submit_signup(request)`: Handles user registration. Checks if the provided email exists in the database and creates a new user profile if it doesn't. Logs the user in after successful registration.
- `submit_signin(request)`: Handles user login. Authenticates the user and checks if they have set up 2FA. Redirects to 2FA setup if not already set up.

## Two-Factor Authentication Setup

The application uses the following views and functions to set up 2FA:

- `setup_2fa(request)`: Generates a TOTP secret key, saves it to the `TOTPDevice`, and sends the key to the user's email for setup. The `TOTPDevice` is initially marked as unconfirmed.
- `verify_2fa(request)`: Allows the user to verify the 2FA setup by providing the TOTP code sent to their email. If the code is correct, the `TOTPDevice` is marked as confirmed.

### Protected Routes

The application includes protected routes that are only accessible to authenticated users:

- `protected(request)`: A protected route that can only be accessed by users who are authenticated.

## Usage

### User Registration

1. Access the registration page by navigating to `/sign_up`.
2. Provide a unique username, email, and password.
3. Submit the registration form.
4. If the email already exists, an error message is displayed.
5. Upon successful registration, you are logged in and redirected to the homepage.

### User Login

1. Access the login page by navigating to `/log_in`.
2. Provide your username and password.
3. Submit the login form.
4. If login is successful, you are redirected to the 2FA setup page if 2FA is not already set up.

### Two-Factor Authentication Setup

1. Access the 2FA setup page by navigating to `/2fa_setup`.
2. A TOTP secret key is generated and sent to your email.
3. Enter the code sent to your email to confirm 2FA setup.
4. Upon successful setup, you are redirected to the homepage.

### Protected Routes

1. Access protected routes by navigating to `/protected`.
2. These routes can only be accessed by authenticated users who have made an account.

### Logout

- To log out, access the `/logout` route. You will be redirected to the homepage.****


# Conclusion

By following these steps, you should be able to set up a basic protected area with email verification option in your Django website project.
