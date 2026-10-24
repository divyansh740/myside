from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# class Enquiry(models.Model):
#     name = models.CharField(max_length=100)
#     phone = models.CharField(max_length=15)
#     email = models.EmailField()
#     course = models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.name} - {self.course}"

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)  # Price in Rupees
    image = models.ImageField(upload_to='courses/', blank=True, null=True)

    def __str__(self):
        return self.title



class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"


import random
from django.db import models
from django.contrib.auth.models import User

class EmailOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_otp(self):
        otp_code = str(random.randint(100000, 999999))
        self.otp = otp_code
        self.save()
        return otp_code

class Enquiry(models.Model):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    course = models.CharField(max_length=100)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.course}"