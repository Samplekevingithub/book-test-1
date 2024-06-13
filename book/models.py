from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_admin= models.BooleanField('Is admin', default=False)
    is_user= models.BooleanField('Is user', default=True)


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category=models.CharField(max_length=100)
    page_count = models.IntegerField()
    isbn = models.CharField(max_length=20, unique=True)
    image= models.ImageField(upload_to="book/images",default="")
    def __str__(self):
        return self.title +'  '+ str(self.id)

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_user': True})
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rental_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fee=models.CharField(max_length=50)
    
    