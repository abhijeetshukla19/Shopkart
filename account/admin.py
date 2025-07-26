from django.contrib import admin
from .models import CustomUser, Seller, Customer

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'contact', 'is_staff', 'is_active')
    ordering = ('username',)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email','contact','dob','gender','profile_picture')
    ordering = ('username',)

class SellerAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email','contact','business_name','business_address','business_landmark','business_pincode','product_category','business_website')
    ordering = ('username',)


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Seller, SellerAdmin)