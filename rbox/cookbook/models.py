from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=42)
    bio = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=42)
    description = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    req_time = models.CharField(max_length=42)
    instructions = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='loguser')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe')
    star = models.BooleanField(default=False)
