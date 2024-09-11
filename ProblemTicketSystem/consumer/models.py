from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
import random

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    title = models.CharField(max_length=300)
    department = models.CharField(max_length=100, default='Unassigned')
    description = models.TextField()
    ticket_number = models.IntegerField(null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ticket_status = models.CharField(max_length=100 , default='pending')
    
    def __str__(self):
        return self.title

# Function to generate a random 5-digit number
def generate_unique_ticket_number():
    return random.randint(10000, 99999)

# Signal to generate a unique ticket_number before saving
@receiver(pre_save, sender=Ticket)
def auto_generate_ticket_number(sender, instance, **kwargs):
    if instance.ticket_number is None:  # Only generate a number if one isn't already set
        ticket_number = generate_unique_ticket_number()

        # Ensure the ticket_number is unique
        while Ticket.objects.filter(ticket_number=ticket_number).exists():
            ticket_number = generate_unique_ticket_number()

        instance.ticket_number = ticket_number
