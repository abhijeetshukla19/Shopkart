from django import forms
from .models import Customer,Seller,PRODUCT_CATEGORY_CHOICES
from django.contrib.auth.forms import UserCreationForm

class CustomerCreationForm(UserCreationForm): 
        
    class Meta:
        
        model = Customer
        fields = ['username', 'first_name', 'last_name', 'email','contact','dob','gender','profile_picture']

        widgets = {
           
            # 'address': forms.TextInput(attrs={'placeholder':'Building / flat no.','class':'form-control','required':'True'}),
            # 'landmark': forms.TextInput(attrs={'placeholder':'area / nearby','class':'form-control','required':'True'}),
            # 'pincode': forms.TextInput(attrs={'placeholder':'6 digit pincode','class':'form-control','required':'True'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'dob':forms.DateInput(attrs={"class":"form-control",'required':'True','type':'date'}),
            'gender':forms.Select(choices=(('male','Male'),('female','Female'),('others','Others')), attrs={'class':'form-control','required':'True'})
        }


    def save(self,commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    


class SellerCreationForm(UserCreationForm): 
        
   
    class Meta:
        model = Seller
        fields = ['username', 'first_name', 'last_name', 'email','contact','business_name','business_address','business_landmark','business_pincode','product_category','business_website']

        widgets = {
           
            'business_name': forms.TextInput(attrs={'placeholder':'Business name','class':'form-control','required':'True'}),
            'business_address': forms.TextInput(attrs={'placeholder':'Building / flat no.','class':'form-control','required':'True'}),
            'business_landmark': forms.TextInput(attrs={'placeholder':'area / nearby','class':'form-control','required':'True'}),
            'business_pincode': forms.TextInput(attrs={'placeholder':'6 digit pincode','class':'form-control','required':'True'}),
            'product_category': forms.Select(choices=PRODUCT_CATEGORY_CHOICES,attrs={'class':'form-control'}),
            'business_website': forms.URLInput(attrs={'placeholder':'Enter business wenbsite','class':'form-control','required':'True'}),
        }


    def save(self,commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


from django import forms

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='Enter your email address')

