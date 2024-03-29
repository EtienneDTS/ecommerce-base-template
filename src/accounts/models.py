from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=5, blank=True)
    phone_number = models.CharField(max_length=10, blank=True)
    is_email_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        if self.username:
            return self.username
        else:
            return "Anonymous"
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = f"{self.first_name} {self.last_name[0]}"
        super().save(*args, **kwargs)   

class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    