from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Offer(models.Model):
    name = models.CharField(max_length=200, unique=True)
    link = models.CharField(max_length=10, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Question(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()

class About(models.Model):
    short_description = models.TextField()
    full_description = models.TextField()

    def __str__(self):
        return self.short_description

    def save(self, *args, **kwargs):
        if About.objects.exists() and not self.pk:
            raise ValidationError('There can be only one instance')
        return super(About, self).save(*args, **kwargs)


class Message(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now=True, editable=False)
    is_client = models.BooleanField(editable=False)


class OrderManager(models.Manager):
    def create_order(self, type, info, client):
        order = self.create(type=type, primary_info=info, client=client)
        order.readiness = 0
        return order


class Order(models.Model):
    type = models.CharField(max_length=10, editable=False)
    primary_info = models.TextField()
    readiness = models.IntegerField(null=True, validators=[MaxValueValidator(100),
                                                           MinValueValidator(0)])  # степень готовности от 0 до 100
    messages = models.ManyToManyField(Message)
    client = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.type

    objects = OrderManager()



