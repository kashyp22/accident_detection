from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class hospital_table(models.Model):
    name=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    email=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    post=models.BigIntegerField()
    district=models.CharField(max_length=100)
    logo=models.CharField(max_length=200)
    status=models.CharField(max_length=100)
    latitude=models.FloatField()
    longitude=models.FloatField()
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)

class ambulance_table(models.Model):
    registration_no=models.CharField(max_length=50)
    drivers_name=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    email = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.CharField(max_length=100)
    act_status = models.CharField(max_length=100,default="pending")
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)
    rc=models.FileField()

class user_table(models.Model):
    LOGIN = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    phone = models.BigIntegerField()
    email = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    pincode = models.IntegerField()
    district = models.CharField(max_length=100)
    photo=models.FileField()
    latitude = models.FloatField()
    longitude = models.FloatField()

class rating_table(models.Model):
    rating=models.FloatField()
    date=models.DateField()
    review=models.CharField(max_length=100)
    USER=models.ForeignKey(user_table,on_delete=models.CASCADE)

class complaint_table(models.Model):
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)
    complaint=models.CharField(max_length=100)
    date=models.DateField()
    reply=models.CharField(max_length=100)

class chat_tabele(models.Model):
    message=models.CharField(max_length=50)
    date = models.DateField()
    FROM_ID=models.ForeignKey(User,on_delete=models.CASCADE,related_name="from_id")
    TO_ID=models.ForeignKey(User,on_delete=models.CASCADE,related_name="to_id")

class notification_table(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    date = models.DateField()
    photo = models.FileField()
    USER = models.ForeignKey(user_table, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)

class accident_report_table(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    date = models.DateField()
    photo = models.FileField(upload_to="accidents/")
    status = models.CharField(max_length=100)
    view_status=models.BooleanField(default=False)

    USER = models.ForeignKey(user_table, on_delete=models.CASCADE)
    AMBULANCE = models.ForeignKey(
        ambulance_table, on_delete=models.CASCADE, null=True, blank=True
    )
    HOSPITAL = models.ForeignKey(
        hospital_table, on_delete=models.CASCADE, null=True, blank=True
    )


class medical_report_table(models.Model):
    report=models.CharField(max_length=250)
    date = models.DateField()
    HOSPITAL=models.ForeignKey(hospital_table,on_delete=models.CASCADE)
    ACCIDENT=models.ForeignKey(accident_report_table,on_delete=models.CASCADE)











