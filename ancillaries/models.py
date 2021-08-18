from django.db import models


class Departments(models.Model):
    """ Departments Model """
    department_name = models.CharField(max_length=100)

    def __str__(self):
        return self.department_name

    class Meta:
        verbose_name_plural = "Departments"


class Locations(models.Model):
    """ Locations Model """
    location_name = models.CharField(max_length=100)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)

    def __str__(self):
        return self.location_name

    class Meta:
        verbose_name_plural = "Locations"


class Suppliers(models.Model):
    """ Suppliers Model """
    supplier_name = models.CharField(max_length=100)

    def __str__(self):
        return self.supplier_name

    class Meta:
        verbose_name_plural = "Suppliers"
