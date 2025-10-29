from django.db import models
from django.contrib.auth.models import User

# Create your models here.

RATING_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)

class Package(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.CharField(max_length=50)
    price = models.IntegerField()
    itinerary = models.ManyToManyField('Itinerary')
    image = models.ManyToManyField('Image')
    date = models.DateField(null=True , blank=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    title: str = models.CharField(max_length=225, blank=True, null=True)
    file = models.FileField(upload_to='images')

    def __str__(self):
        return self.title


class Itinerary(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField()

    def __str__(self):
        return self.title


class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Review(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, null=True , blank=True)
    stars = models.IntegerField(choices=RATING_CHOICES,null=True , blank=True)
    review=models.TextField(null=True , blank=True)

    def __str__(self):
        return self.registration.user.username


class Feedback(models.Model):
    user = models.ForeignKey(
        User , on_delete=models.CASCADE , null=True , blank=True)
    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, null=True, blank=True)
    feedback = models.TextField()

    def __str__(self):
        return self.user.username

class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return 'Message from ' + self.name
    