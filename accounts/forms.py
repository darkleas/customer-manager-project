from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm,User
from django.contrib.auth.models import User
from .models import Order,Customer,Product
from django import forms
from django.core.exceptions import ValidationError
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
class CustomerForm(ModelForm):
    password = forms.CharField(max_length=250,widget=forms.PasswordInput)
    class Meta:
        model = Customer
        fields = ['name','phone','email','password']
        exclude = ['user']
        widgets = {
            'phone': PhoneNumberInternationalFallbackWidget(),
        }

    
class ProfilePictureForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['profile_pic']
    def clean(self):
        image = self.cleaned_data.get('profile_pic', False)
        if image:
            if image.size > 4*1024*1024:
                raise ValidationError("Image file too large. please upload lower than 2MB")
        else:
            raise ValidationError("Couldn't read uploaded image")
    

class ResetPasswordForm(forms.Form):
    password = forms.CharField(max_length=250,widget=forms.PasswordInput)
    repassword = forms.CharField(max_length=250,widget=forms.PasswordInput)
    confirmpassword = forms.CharField(max_length=250,widget=forms.PasswordInput)
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        repassword = cleaned_data.get('repassword')
        if password and repassword and password != repassword:
            raise forms.ValidationError("Passwords isn't same")

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['product'] 
class OrderUpdateForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
                
class CreateUserForm(forms.Form,UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']
