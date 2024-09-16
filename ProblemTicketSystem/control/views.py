from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
import pytz #used to take time zone in india 
from consumer.models import Ticket
from django.core.paginator import Paginator
from django.views import View

@login_required
def rejected(request):
    if request.user.is_authenticated and request.user.username == 'admin':
        username = "Muhammed Shahil KP"
        Uticket = Ticket.objects.filter(ticket_status="rejected")
        if Uticket.exists():
            paginator = Paginator(Uticket, 2)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'Aindex/aindex.html', {'data': username, 'page_obj': page_obj})
        else:
            return HttpResponse("No Assigned tickets found.", status=404)
    else:
        return HttpResponse("You are not authorized to access this page.", status=403)
    
@login_required
def assigned(request):
    if request.user.is_authenticated and request.user.username == 'admin':
        username = "Muhammed Shahil KP"
        Uticket = Ticket.objects.filter(ticket_status="assigned")
        if Uticket.exists():
            paginator = Paginator(Uticket, 2)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'Aindex/aindex.html', {'data': username, 'page_obj': page_obj})
        else:
            return HttpResponse("No Assigned tickets found.", status=404)
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


class ProblemDetailView(LoginRequiredMixin,View):
    
    def get(self, request, ticket_id):
        username = "Muhammed Shahil KP"
        ticket = get_object_or_404(Ticket, ticket_number=ticket_id)

        # Convert updated_at to IST (only for display, not modifying DB)
        if ticket.updated_at:
            indian_tz = pytz.timezone('Asia/Kolkata')
            ticket.updated_at_ist = ticket.updated_at.astimezone(indian_tz)  # Convert UTC to IST for display

        return render(request, 'ProbUpdation/ProbUpdation.html', {
            'ticket': ticket,
            'data': username,
            'updated_at_ist': ticket.updated_at_ist if ticket.updated_at else None
        })
    
    def post(self, request, ticket_id):
        username = "Muhammed Shahil KP"
        ticket = get_object_or_404(Ticket, ticket_number=ticket_id)

        # Get the form data
        new_status = request.POST.get('status')
        new_action_taken = request.POST.get('actiontaken')

        # Only update the ticket if there's a status or action change
        if new_status != ticket.ticket_status or new_action_taken != ticket.action_taken:
            # Update the ticket fields
            ticket.ticket_status = new_status
            ticket.action_taken = new_action_taken
            ticket.last_updated_by = request.user

            # Capture the current time in UTC
            ticket.updated_at = timezone.now()  # Save in UTC

            ticket.save()

        return redirect('control:problemview', ticket_id=ticket.ticket_number)