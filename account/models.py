from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator,RegexValidator

# Create your models here.
class CustomUser(AbstractUser):
    contact = models.CharField(max_length=10,blank=True,null=True)
    groups = models.ManyToManyField('auth.Group',related_name="account_user_set",blank=True)
    user_permissions = models.ManyToManyField('auth.Permission',related_name='account_user_permission_set',blank=True)

    def __str__(self):
        return self.username  

    class Meta:
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']), 
        ]

class Customer(CustomUser):
    # address = models.CharField(max_length=255)
    # landmark = models.CharField(max_length=255)
    # pincode = models.CharField(max_length=6,validators=[MinLengthValidator(6),RegexValidator(r'^\d{6}$','Enter a Valid 6 digit pincode')])
    profile_picture = models.ImageField(upload_to='profile_pics/',null=True,blank=True)
    dob = models.DateField()
    gender = models.CharField(max_length=10,choices=(('male','Male'),('female','Female'),('others','Others')))



    def __str__(self):
        return f'Customer : {self.first_name} {self.last_name}'
    
    class Meta:
        db_table = 'Customer'


PRODUCT_CATEGORY_CHOICES = [
        ('electronics','ELECTRONICS'),
        ('fashion','FASHION'),
        ('home_appliances','HOME APPLIANCES'),
        ('books','BOOKS'),
        ('beauty','BEAUTY'),
        ('sports','SPORTS'),
        ('toys','TOYS'),
        ('other','OTHER'),
    ]
    

class Seller(CustomUser):
   
    business_name = models.CharField(max_length=255)
    business_address = models.CharField(max_length=255)
    business_landmark = models.CharField(max_length=255)
    business_pincode = models.CharField(max_length=6,validators=[MinLengthValidator(6),RegexValidator(r'^\d{6}$','Enter a Valid 6 digit pincode')])
    product_category = models.CharField(max_length=25,choices=PRODUCT_CATEGORY_CHOICES)
    business_website = models.URLField(null=True,blank=True)

    def __str__(self):
        return f'Seller : {self.first_name} {self.last_name}, {self.business_name}'
    
    class Meta:
        db_table = 'Seller'