from django.db import models

class Ticket(models.Model):
    title = models.CharField(max_length=300)
    department = models.CharField(max_length=100, default='Unassigned')
    description = models.TextField()
    ticket_number = models.IntegerField(null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    
    def __str__(self):
        return self.title
