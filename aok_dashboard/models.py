from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Business(models.Model): 
    
    brand_name = models.CharField(max_length=100)
    slogan = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', blank=True)
    description = models.TextField(blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    latitude = models.CharField(max_length=50, blank=True)
    longitude = models.CharField(max_length=50, blank=True)

    def __str__(self):  
        return self.brand_name

class MenuItem(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='menu_items')
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.category})"


class GalleryImage(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Gallery Image {self.id} for {self.business.brand_name}"

DAYS_OF_WEEK = [
    ('sunday', 'Sunday'),
    ('monday', 'Monday'),
    ('tuesday', 'Tuesday'),
    ('wednesday', 'Wednesday'),
    ('thursday', 'Thursday'),
    ('friday', 'Friday'),
    ('saturday', 'Saturday'),
]

class BusinessHour(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='hours')
    day = models.CharField(max_length=20, choices= DAYS_OF_WEEK)
    from_time = models.TimeField(null=True, blank=True)
    to_time = models.TimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta: 
        unique_together = ('business', 'day')
        ordering = ['day']

    def __str__(self):
        if self.is_closed:
            return f"{self.day.title()}: Closed"
        return f"{self.day.title()}: {self.from_time} - {self.to_time}"

class Balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance_from_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance_from_tips = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    @property
    def current_balance(self):
        return self.balance_from_sales + self.balance_from_tips

    def __str__(self):
        return f"Balance for {self.user.username}"


class AOKPoint(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"AOK Points for {self.user.username}"