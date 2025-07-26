from django.db import models
from account.models import Customer, CustomUser,Seller
from django.core.validators import RegexValidator

# Create your models here.

class Category(models.Model):
    name =  models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock_qty= models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_pics/')
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at= models.DateField(auto_now=True)

    def __str__(self):
        return self.title



class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=50)
    landmark = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state= models.CharField(max_length=50)
    pincode = models.CharField(max_length=6,validators=[RegexValidator(r'^\d{6}$','Enter a valid 6 digit pincode')])


class Order(models.Model):
    order_id = models.CharField(max_length=50,primary_key=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)

    shipping_address = models.ForeignKey(ShippingAddress,on_delete=models.CASCADE)

    payment_status = models.CharField(max_length=20,choices=(('paid','Paid'),('unpaid','Unpaid')),default='unpaid')

    order_status = models.CharField(max_length=20,choices=(('pending','Pending'),('shipped','Shipped'),('delivered','Delivered')),default='pending')

    order_amount= models.DecimalField(max_digits=10,decimal_places=2)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10,decimal_places=2)


class Cart(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)