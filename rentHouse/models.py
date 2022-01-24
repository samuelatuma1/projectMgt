from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    status = models.CharField(max_length=250, default='Hello there, I am available', blank=True, null=True)
    
    img = models.ImageField(upload_to='profiles/images/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} profile"

class State(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class HouseType(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
class Region(models.Model):
    name = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name} in {self.state}"
    
class UploadHouse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='houses')
    photo = models.ImageField(upload_to='houses/')
    desc = models.TextField()
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='houses')
    
    house_type = models.ForeignKey(HouseType, on_delete=models.CASCADE)
    price = models.IntegerField()
    
    bill_period = [("monthly", "monthly"), ("quaterly", "quaterly"), ("yearly", "yearly")]
    
    billed = models.CharField(max_length=15, choices=bill_period, default='yearly')
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    
    display = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.house_type} in {self.region}, {self.state} by {self.user}"