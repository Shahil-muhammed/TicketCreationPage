from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
import logging
from .models import Ticket  # Import your Ticket model
from .forms import TicketForm

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            new_ticket = form.save()  # Save the form data to the database

            # Add a success message with the ticket number
            messages.success(
                request,
                f'Problem is now notified to the admin. Please note the ticket number for further reference. Your ticket number is "{new_ticket.ticket_number}".'
            )
            
            return redirect('index')  # Redirect to the index page after saving
    else:
        form = TicketForm()
    
    data = [
        {
            'title': 'Track Existing Problem',
            'description': 'Enter your problem ID to track the status of your issue.',
            'image': 'search.jpg',
            'pit': 'Problem ID',
            'epit': 'Enter Problem ID',
            'description_field': False,  
            'button': 'Track Problem'
        },
        {
            'title': 'Create New Problem',
            'description': 'Describe your issue in detail and submit it to get assistance.',
            'image': 'Problem.jpg',
            'pit': 'Problem Title',
            'epit': 'Enter Title',
            'description_field': 'Enter description for your issue',  
            'edescription': 'Describe the issue',  
            'button': 'Submit Problem'
        }
    ]

    return render(request, 'index/index.html', {'data': data, 'form': form})

def problem(request, pid):
    try:
        pid = int(pid)  # Convert pid to an integer
    except ValueError:
        messages.error(request, "Invalid Problem ID. Please enter a valid number.")
        return redirect('index')  # Redirect to index or a custom error page
    
    try:
        # Fetch the ticket from the database using the Ticket model
        ticket = Ticket.objects.get(ticket_number=pid)
        logger = logging.getLogger("TESTING")
        logger.debug(f'Fetched ticket: {ticket}')
        
        # Determine status class based on the ticket's status
        status_class = get_status_class(ticket.department)  # Adjust if department is used for status
        
        # Prepare the data dictionary for the template
        result = {
            'id': ticket.id,
            'title': ticket.title,
            'description': ticket.description,
            'status': ticket.department,  # Assuming 'department' is being used as a status
            'action': 'Action details here',  # Replace with actual action if you have such a field
            'status_class': status_class
        }
    
    except Ticket.DoesNotExist:
        # Set result to None or empty dictionary if no ticket is found
        messages.error(request, "Problem ID does not exist. Please check the ID and try again.")
        result = {}  
        
    return render(request, 'track/trackingdata.html', {'data': result})

def get_status_class(status):
    if status == 'under investigation':
        return 'bg-warning text-dark'
    elif status == 'rejected':
        return 'bg-danger text-white'
    elif status == 'resolved':
        return 'bg-success text-white'
    else:
        return 'bg-secondary text-white'
