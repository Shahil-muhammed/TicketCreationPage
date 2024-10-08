from django.urls import reverse_lazy
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from .forms import AssignerLoginForm,AssignerSignupForm
from django.http import HttpResponse
from consumer.models import Ticket
from django.views import View as v
from django.utils import timezone
import pytz #used to take time zone in india 
from django.core.paginator import Paginator
from django.db.models import Q #for to check multiple conditions in get_objext_or_404
# Create your views here.
def vendor(request):
    return HttpResponse("Vendor Url called ")

from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import AssignerSignupForm
from django.contrib.auth.models import User

class AssignerSignupView(CreateView):
    model = User 
    form_class = AssignerSignupForm
    template_name = 'auth/signup.html'
    success_url = reverse_lazy('assigner:assigner-login')  

    def form_valid(self, form):
        form.save()  # Save the form
        return super().form_valid(form)  # Redirect to the login page after successful signup

        
class AssignerLoginView(LoginView):
    form_class = AssignerLoginForm
    def get_success_url(self):
        return reverse_lazy('assigner:vendor') 
    template_name = 'auth/login.html'

    def validform(self,form):
        # Custom login logic if needed
        return super().form_valid(form)
    
   
    
class AssignerLogoutView(LogoutView):
    next_page = reverse_lazy('assigner:assigner-login')  # Redirect to login after logout

class ProblemDetailView(LoginRequiredMixin,v):
    
    def get(self, request, ticket_id):
        if request.user.username.endswith('_localstaff'):
            username = request.user.username.replace('_localstaff','')
            ticket = get_object_or_404(Ticket, Q(ticket_number=ticket_id) & (Q(ticket_status='assigned') | Q(ticket_status='lsolved')))
        else:
            return HttpResponse("Your not an local staff of this company sorry !!!")

        # Convert updated_at to IST (only for display, not modifying DB)
        if ticket.updated_at:
            indian_tz = pytz.timezone('Asia/Kolkata')
            ticket.updated_at_ist = ticket.updated_at.astimezone(indian_tz)  # Convert UTC to IST for display

        return render(request, 'Aprob/Aprob.html', {
            'ticket': ticket,
            'data': username,
            'updated_at_ist': ticket.updated_at_ist if ticket.updated_at else None
        })
    
    def post(self, request, ticket_id):
        #username = "Muhammed Shahil KP"
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

        return redirect('assigner:viewprob', ticket_id=ticket.ticket_number)

class Lsolved(LoginRequiredMixin,v):
    def get(self,request, ticket_id):
        if request.user.username.endswith('_localstaff'):
            username = request.user.username.replace('_localstaff','')
            ticket= get_object_or_404(Ticket,ticket_number=ticket_id,ticket_status='lsolved')
        else:
            return HttpResponse("Your not an local staff of this company sorry !!!")
        
        if ticket.updated_at:
            indian_tz = pytz.timezone('Asia/Kolkata')
            ticket.updated_at_ist = ticket.updated_at.astimezone(indian_tz)

        return render(request,'Aprob/Aprob.html',{'ticket':ticket,'data':username,'updated_at_ist':ticket.updated_at_ist})
    

class AssignerSolvedTickets(LoginRequiredMixin,v):
    def get(self,request):
        if request.user.username.endswith('_localstaff'):
            username=request.user.username.replace('_localstaff','')
            aticket=Ticket.objects.filter(ticket_status='lsolved')

            if aticket.exists():
                paginator = Paginator(aticket, 4)  # Pagination
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                return render(request, 'Aindex/aindex.html', {'page_obj': page_obj, 'data': username , 'local':True})
            else:
                return HttpResponse("Solved ticket not found")

