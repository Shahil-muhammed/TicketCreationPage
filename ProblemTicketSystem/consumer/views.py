from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages  # Import the messages framework
import logging
from .forms import TicketForm

# Simulated data for testing
problem_list = [
    {
        'id': 123,
        'title': 'First issue 123 fetched successfully',
        'description': 'Bad behaviour from restaurant employee named x, he has misbehaved with me many times',
        'status': 'under investigation',
        'action': 'We will suspend the employee if any issues are found'
    },
    {
        'id': 456,
        'title': 'Second issue 456 fetched successfully',
        'description': 'Bad behaviour from restaurant employee named y, he is misbehaving with me many times',
        'status': 'rejected',
        'action': 'No suspicious activities found during CCTV investigation'
    }
]

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
        return HttpResponse("Invalid Problem ID", status=400)
    
    result = next((item for item in problem_list if item['id'] == pid), None)
    logger = logging.getLogger("TESTING")
    logger.debug(f'variable value is {result}')
    
    if result:
        # Determine status class based on the problem status
        result['status_class'] = get_status_class(result['status'])
    else:
        result = {}  # Ensure result is an empty dictionary if no data found
    
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
