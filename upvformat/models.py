from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(
           settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
           
    def __str__(self):
        return f'UserProfile of {self.user.username}'
    
class Conversion(models.Model):
    input_text = models.TextField()
    output_text = models.TextField()

class Numeric(models.Model):
    question_text = models.TextField(max_length=200)
    gift_format = models.TextField()

    def __str__(self):
        return self.question_text


