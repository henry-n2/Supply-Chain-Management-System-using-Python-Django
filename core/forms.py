from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ManufacturerProduct, DistributorStock

class RetailerSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'RETAILER'
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class CustomerSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'CUSTOMER'
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class ManufacturerProductForm(forms.ModelForm):
    class Meta:
        model = ManufacturerProduct
        fields = ('name', 'description', 'image', 'base_price', 'min_quantity', 'available_quantity')


# class DistributorSignUpForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.role = 'DISTRIBUTOR'
#         if commit:
#             user.save()
#         return user
    

class DistributorSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'DISTRIBUTOR'
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user   
# class DistributorStockForm(forms.Form):
#     quantity = forms.IntegerField(min_value=1)
#     price = forms.DecimalField(min_value=0.01)


from django import forms
from .models import DistributorStock

class DistributorStockForm(forms.ModelForm):  # Change from forms.Form to ModelForm
    class Meta:
        model = DistributorStock
        fields = ['price', 'available_quantity']




from django import forms
from .models import RetailerStock

class RetailerStockForm(forms.ModelForm):
    class Meta:
        model = RetailerStock
        fields = ['product', 'price', 'available_quantity']