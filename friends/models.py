from django.db import models
from users.models import PinklerUser

class FriendshipRequest(models.Model):
    SENT = 'sent'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    STATUS_CHOICES = [
        (SENT, 'Sent'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]
    created_by = models.ForeignKey(PinklerUser, related_name='sent_requests', on_delete=models.CASCADE)
    created_for = models.ForeignKey(PinklerUser, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=SENT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_by} to {self.created_for} - {self.status}"