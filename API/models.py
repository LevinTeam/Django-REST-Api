from django.db import models


# Create your models here.
class CommentsData(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    subject = models.CharField(max_length=40)
    message = models.TextField(max_length=500)


class Users(models.Model):
    firstname = models.CharField(max_length=40)
    lastname = models.CharField(max_length=40)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    password = models.CharField(max_length=200)
