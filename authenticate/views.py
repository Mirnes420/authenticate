from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.db import IntegrityError


# home view/ first page

def homepage(request):
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
        username = request.POST.get('username')
        password = request.POST.get('password')
        # signing in using django authenticate method for checking the user data
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # used djangos login method for starting a user session
            login(request, user)
            return render(request, 'authenticate/home.html', {'user': request.user})
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
            # creating user profile if it does not already exist using django User model and saving it in the database
            user = User.objects.create_user(username=username,email=email, password=password)
            user.save()
            login(request, user)
            return HttpResponseRedirect('allowed')
        except IntegrityError:
             # throw an error if user already exist
             return render(request, 'authenticate/sign_up.html', {'error': 'User already exist.'})

# succes page when user creates a new profile

def allowed(request):
    return render(request, 'authenticate/allowed.html')

# using @login_method to protect certain pages from non-authorised users //goal of the task//

@login_required
def protected(request):
    return render(request, 'authenticate/protected.html')

# logout function that ends user section and returns the user to the homepage

def logout_view(request):
    logout(request)
    return redirect('home')

