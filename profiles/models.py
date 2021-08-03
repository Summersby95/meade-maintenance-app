from django.db import models
from django.contrib.auth.models import User
from ancillaries.models import Departments


class UserTypes(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name_plural = "User Types"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    user_type = models.ForeignKey(UserTypes, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.username