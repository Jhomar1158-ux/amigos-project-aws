from django.db import models

# Create your models here.

class user(models.Model):
    name=models.CharField(default="Name*", max_length=255)
    alias=models.CharField(default="Alias*", max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    day_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class amigos(models.Model):
    llave=models.ForeignKey(user,related_name = 'llave_user', on_delete = models.CASCADE, null=True)
    friends=models.ManyToManyField(user, related_name="friendss")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

