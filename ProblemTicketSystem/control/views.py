from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from consumer.models import Ticket
from django.core.paginator import Paginator
import logging

@login_required  # Ensures the user is logged in
def SecondAdmin(request):
    if request.user.is_authenticated and request.user.username == 'admin':
        username = "Muhammed Shahil KP"
        Uticket = Ticket.objects.all()
        
        # Pagination: Show 2 tickets per page (we can adjust as needed)
        paginator = Paginator(Uticket, 2)
        # Get the current page number from the URL query parameter '?page='
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Logging
        logger = logging.getLogger("TESTING")
        logger.debug(f'Fetched ticket: {Uticket}')

        # Render the page with paginated tickets
        return render(request, 'Aindex/aindex.html', {'data': username, 'page_obj': page_obj})
    else:
        # If not authorized, redirect to an error page or display a message
        return HttpResponse("You are not authorized to access this page.", status=403)
