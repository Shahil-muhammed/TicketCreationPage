from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
import logging
from .models import Ticket  # Import your Ticket model
from .forms import TicketForm
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import ConsumerSignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

@login_required
# Create your views here.
def index(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, user=request.user)
        if form.is_valid():
            new_ticket = form.save()  # Save the form data to the database

            # Add a success message with the ticket number
            messages.success(
                request,
                f'Problem is now notified to the admin. Please note the ticket number for further reference. Your ticket number is "{new_ticket.ticket_number}".'
            )
            
            return redirect('consumer:index')  # Redirect to the index page after saving
    else:
        form = TicketForm()
        username = request.user.username if request.user.is_authenticated else None
    
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

    return render(request, 'index/index.html', {'data': data, 'form': form , 'uname':username})

def problem(request, pid):
    try:
        pid = int(pid)  # Convert pid to an integer
    except ValueError:
        # Handle invalid problem ID if it's not an integer
        messages.error(request, "Invalid Problem ID. Please enter a valid number.")
        return redirect('index')
    
    if not Ticket.objects.filter(ticket_number=pid).exists():
        # If the ticket does not exist, return a custom error message or redirect
        messages.error(request, "Problem ID does not exist. Please check the ID and try again.")
        return redirect('index')
    # Fetch the ticket or return a 404 if it doesn't exist
    ticket = get_object_or_404(Ticket, ticket_number=pid)  # Use 'ticket_number', assuming 'pid' is actually the ticket_number
    
    # Log the fetched ticket
    logger = logging.getLogger("TESTING")
    logger.debug(f'Fetched ticket: {ticket}')
    
    # Determine the status class based on ticket status
    status_class = get_status_class(ticket.ticket_status)
    
    # Get the username of the logged-in user, if authenticated
    username = request.user.username if request.user.is_authenticated else None
    
    # Prepare the result data for the template
    result = {
        'id': ticket.id,
        'title': ticket.title,
        'description': ticket.description,
        'status': ticket.ticket_status,
        'action': ticket.action_taken,
        'status_class': status_class
    }

    return render(request, 'track/trackingdata.html', {'data': result, 'uname': username})

def get_status_class(status): 
    if status == 'pending':
        return 'bg-warning text-dark'
    elif status == 'rejected':
        return 'bg-danger text-white'
    elif status == 'resolved':
        return 'bg-success text-white'
    elif status == 'assigned':
        return 'bg-primary text-white'
    else:
        return 'bg-secondary text-white'


# SignUp view for new users
class SignUpView(CreateView):
    form_class = ConsumerSignUpForm
    template_name = 'signup/signup.html'
    success_url = reverse_lazy('consumer:signin')

# SignIn view for existing users

class SignInView(LoginView):
    template_name = 'signin/signin.html'

    def form_valid(self, form):
        user = form.get_user()
        if user.username == 'admin' and form.cleaned_data.get('password') == 'Ads2233@#1':
            login(self.request, user)
            return redirect('control:SecondAdmin')  # Redirect to the control app's admin view
        elif user.is_authenticated and user.username != 'admin':
            login(self.request, user)
            return redirect('consumer:index')  # Redirect to consumer app's index view
        return super().form_valid(form)
    
def custom_logout(request):
    logout(request)
    return redirect('consumer:index') 

