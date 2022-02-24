from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):

    """ This class inherits base User creation form and adds extra field of email """
    email=forms.EmailField()

    class Meta:
        """ Meta is basically used to change the behavior of your model fields like changing
         order options,verbose_name and lot of other options"""

        model=User

        fields = ['username','email','password1','password2']

        ## Over-riding error message for username field  
        error_messages={
            'username':{'unique':'This user is taken '}
        }
    
    def clean_email(self):
        """ Function based validator for email """

        email=self.cleaned_data.get('email')

        if 'gmail' not in email:

            raise forms.ValidationError('Please enter only gmail domain name for the mail ID')
        
        return email


class UserUpdateForm(forms.ModelForm):
    ''' ModelForms are used to work with databse by updating them using user inputs,.
        Here we have defined fields to update name and mail Id of user '''
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']