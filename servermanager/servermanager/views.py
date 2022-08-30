from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.conf import settings

from django.http import HttpResponse

def main(request):
    print(f"MAIN ")
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    return HttpResponse("OpenTASites")

def health(request):
    return HttpResponse("OpenTASites /health")

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/')
        # Redirect to a success page.
    else:
        return redirect('/')
        # Return an 'invalid login' error message.

def logout_view(request):
    logout(request)
    return HttpResonse("Logged out")
    # Redirect to a success page.
