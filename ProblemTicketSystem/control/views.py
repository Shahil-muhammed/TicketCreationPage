from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required  # Ensures the user is logged in
def SecondAdmin(request):
    if request.user.is_authenticated and request.user.username == 'admin':
        return HttpResponse("Hi, welcome to the second admin page")
    else:
        return HttpResponse("You are not authorized to access this page.", status=403)
