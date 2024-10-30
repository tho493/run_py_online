from django.db import models

# Create your models here.

class test_part(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

class test_case(models.Model):
    id = models.AutoField(primary_key=True)
    test_part = models.ForeignKey(test_part, on_delete=models.CASCADE)
    output = models.CharField(max_length=100)

class variable(models.Model):
    test_case = models.ForeignKey(test_case, on_delete=models.CASCADE)
    var = models.CharField(max_length=100)
    input = models.CharField(max_length=100)