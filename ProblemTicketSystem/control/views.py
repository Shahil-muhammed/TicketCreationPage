from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout

@login_required  # Ensures the user is logged in
def SecondAdmin(request):
    if request.user.is_authenticated and request.user.username == 'admin':
        username = "Muhammed Shahil KP"
        return render (request,'Aindex/aindex.html',{'data':username})
    else:
        return HttpResponse("You are not authorized to access this page.", status=403)
