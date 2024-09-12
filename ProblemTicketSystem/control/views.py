from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from consumer.models import Ticket
from django.core.paginator import Paginator
import logging

@login_required  
def SecondAdmin(request):
    if request.user.is_authenticated and request.user.username == 'admin':
        username = "Muhammed Shahil KP"
        Uticket = Ticket.objects.filter(ticket_status="pending")
        if Uticket.exists():
            paginator = Paginator(Uticket, 2)  # Pagination
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'Aindex/aindex.html', {'page_obj': page_obj, 'data': username})
        else:
            return HttpResponse("No Pending status found ")
    else:
        return HttpResponse("You are not authorized to access this page.", status=403)
    
@login_required
def solved(request):
    if request.user.is_authenticated and request.user.username == 'admin':
        username = "Muhammed Shahil KP"
        Uticket = Ticket.objects.filter(ticket_status="resolved")
        if Uticket.exists():
            paginator = Paginator(Uticket, 2)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'Aindex/aindex.html', {'data': username, 'page_obj': page_obj})
        else:
            return HttpResponse("No resolved tickets found.", status=404)
    else:
        return HttpResponse("You are not authorized to access this page.", status=403)