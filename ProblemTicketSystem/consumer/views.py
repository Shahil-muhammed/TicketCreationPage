from django.shortcuts import render
from django.http import HttpResponse
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
