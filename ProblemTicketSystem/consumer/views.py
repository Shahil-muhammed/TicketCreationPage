from django.shortcuts import render
from django.http import HttpResponse
import logging
# Ensure this is defined at the top of your views.py
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

    return render(request, 'index/index.html', {'data': data})

def problem(request, pid):
    try:
        pid = int(pid)  # Convert pid to an integer
    except ValueError:
        return HttpResponse("Invalid Problem ID", status=400)
    
    result = next((item for item in problem_list if item['id'] == pid), None)
    logger = logging.getLogger("TESTING")
    logger.debug(f'variable value is {result}')
    
    if result:
        # Assign status class based on the problem status
        if result['status'] == 'under investigation':
            result['status_class'] = 'bg-warning text-dark'
        elif result['status'] == 'rejected':
            result['status_class'] = 'bg-danger text-white'
        elif result['status'] == 'resolved':
            result['status_class'] = 'bg-success text-white'
        else:
            result['status_class'] = 'bg-secondary text-white'
    else:
        result = {}  # Ensure result is an empty dictionary if no data found
    
    return render(request, 'track/trackingdata.html', {'data': result})
