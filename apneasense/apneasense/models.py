from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

class Record(models.Model):
    datetime=models.DateTimeField(auto_now_add=True)
    x = ArrayField(ArrayField(ArrayField(models.FloatField(), size=6), size=6000), blank=True, null=True)
    prediction = ArrayField(models.FloatField(), blank=True, null=True)
    signal=models.ImageField(upload_to='signals')
    user=models.ForeignKey(User,on_delete=models.CASCADE)

class Client(models.Model):
    sex = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    age=models.IntegerField()
    email=models.EmailField()
    sex=models.CharField(max_length=6,choices=sex)
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.firstname