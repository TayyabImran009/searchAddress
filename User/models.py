from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class accountsCheck(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.user.username

class userAddress(models.Model):
    fname = models.CharField(max_length=100,null=True,blank=True)
    lname = models.CharField(max_length=100,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    tag = models.CharField(max_length=100,null=True,blank=True)
    is_dataRetrived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.address


class addressDetails(models.Model):
    number = models.IntegerField()
    address = models.ForeignKey(userAddress, on_delete=models.CASCADE, null=True)
    numberChecked = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return str(self.number)

class addressDetailsTags(models.Model):
    tagName = models.CharField(max_length=100)

class detailsTags(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    addressDetails = models.ForeignKey(addressDetails, on_delete=models.CASCADE)
    tags = models.ManyToManyField(addressDetailsTags, blank=True)


