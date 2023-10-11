from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.db import IntegrityError
from django_otp.plugins.otp_totp.models import TOTPDevice
import pyotp
from django.core.mail import send_mail



# home view/ first page

def homepage(request):
    # if user is logged in, redirect him to the page that asks him to verify using email(if not already verified)
    user = request.user 
    if user.is_authenticated:
        return check_totp_device(request)
    # if user is not logged in, he will see a standard home page
    return render(request, 'authenticate/home.html')

# login page

def log_in(request):
    return render(request, 'authenticate/log_in.html')

# signup page

def sign_up(request):
    return render(request, 'authenticate/sign_up.html')

# submit_signin function

def submit_signin(request):
    if request.method == 'POST':
        # get the data
        username = request.POST.get('username')
        password = request.POST.get('password')
        # signing in using django authenticate method for checking the user data
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # used djangos login method for starting a user session
            login(request, user)
            # when user logs in, check if he made 2FA setup and redirect to that view
            return check_totp_device(request)
        else:
            # and returning an error if the user provided the wrong data
            return render(request, 'authenticate/log_in.html', {'error': 'Invalid login! Try again.'})
    else:
        return render(request, 'authenticate/log_in.html')

# submit signup / create a profile function

def submit_signup(request):
    if request.method == 'POST':   
        # getting all the data 
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
           
           # Check if the email already exists in the database
            if User.objects.filter(email=email).exists():
                # return an error if so
                return render(request, 'authenticate/sign_up.html', {'error': 'User with this email already exists.'})
            
            # creating user profile if it does not already exist using django User model and saving it in the database
            user = User.objects.create_user(username=username,email=email, password=password)
            user.save()
            login(request, user)
            return HttpResponseRedirect('allowed')
        except IntegrityError:
             # throw an error if user already exist
             return render(request, 'authenticate/sign_up.html', {'error': 'User already exist.'})

# function that checks if user has verified email
def check_totp_device(request):
    user = request.user

    # Check if the user has a TOTP device
    has_totp_device = TOTPDevice.objects.filter(user=user, confirmed=True).exists()

    context = {
        'has_totp_device': has_totp_device,
    }
    # home returns a different view based on 'context' that has boolean value
    return render(request, 'authenticate/home.html', context)

# function used for generating 2FA code and sending it to user.email
def setup_2fa(request):
    try:
        user = request.user
        global totp_device
        # Check if the user already has a TOTP device
        totp_device = TOTPDevice.objects.filter(user=user).first()
        # Generate a TOTP shared secret key
        totp_secret_key = pyotp.random_base32()
        # confirmed set to False until user confirms secret key in 2fa_setup.py
        totp_device = TOTPDevice.objects.create(user=user, confirmed=False)
        totp_device.email = user.email
        totp_device.save()

        # Send the shared secret key to the user's email
        subject = 'Your Two-Factor Authentication Setup Code'
        message = f'Your 2FA setup code is: {totp_secret_key}'
        from_email = 'm29490596@gmail.com'
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)
        # used in verify_2fa()
        request.session['totp_secret_key'] = totp_secret_key

        return render(request, 'authenticate/2fa_setup.html', {'info': 'the code was sent to ', 'user_email': user.email})
    # Handle case where the user doesn't exist
    except User.DoesNotExist:
        return render(request, 'authenticate/sign_up.html', {'error': 'Create a profile to continue.'}) 

# function that compares provided key with totop_secret_key
def verify_2fa(request):
    if request.method == 'POST':
        # key provided by the user
        totp_code = request.POST.get('totp_code')
        user = request.user

        try:
            
            if totp_code == request.session.get('totp_secret_key'):
                # if user successfully confirms the secret_key, confirm it in totp_device, save changes and return a view with updated data
                totp_device.confirmed = True
                totp_device.save()
                return check_totp_device(request)
            else:
                # if secret_code is incorrect, throwing an error 
                info='Wrong code provided. Check '
                return render(request, 'authenticate/2fa_setup.html', {'info': info, 'user_email': user.email})
        # handle case if no TotpDevice exist for that user
        except TOTPDevice.DoesNotExist:
            info = 'You do not have a TOTP device set up. Please set up 2FA first.'
            return render(request, 'authenticate/2fa_setup.html', {'info': info, 'user_email': user.email})
    else:
        # if request method is get, return a user to homepage based on his totp_device value
        info: None

    return check_totp_device(request)

# succes page when user creates a new profile

def allowed(request):
    return render(request, 'authenticate/allowed.html')

# using @login_required decorator to protect certain pages from non-authorised users //goal of the task//

@login_required
def protected(request):
    return render(request, 'authenticate/protected.html')

# logout function that ends user session and returns the user to the homepage

def logout_view(request):
    logout(request)
    return redirect('home')

