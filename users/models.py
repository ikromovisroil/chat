from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Science(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class User(AbstractUser):
    role = models.ForeignKey(Role,on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='avatars/', default='avatars/default.png', null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    about = models.CharField(max_length=250, null=True, blank=True)


    def __str__(self):
        return self.username


class UserGroup(models.Model):
    role = models.ForeignKey(Role,on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.group}"


class UserScience(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    science = models.ForeignKey(Science, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.science}"


class Chat(models.Model):
    user1 = models.ForeignKey(User,related_name='user1', on_delete=models.CASCADE, null=True, blank=True)
    user2 = models.ForeignKey('users.User',related_name='user2', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='chat/', null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)