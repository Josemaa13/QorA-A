from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    
    def __str__(self):
        return f"[{self.id}]: {self.username}"

class UserRating(models.Model):
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_given')
    rated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_received')
    score = models.IntegerField(default=1) # 1 to 5
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('rater', 'rated_user')

    def __str__(self):
        return f"{self.rater.username} rated {self.rated_user.username}: {self.score}"
