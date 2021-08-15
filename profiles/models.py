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
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    user_type = models.ForeignKey(UserTypes, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

    def get_full_name(self):
        return self.first_name + " " + self.last_name


class UserBonusOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bonus = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "User Bonus Orders"
