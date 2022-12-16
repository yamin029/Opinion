# the purpose of this python file is to create form for the models and render them accordingly
from django.forms import ModelForm
from .models import Room,User
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email' ,'password1','password2', 'avatar']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host','participants']
        
class UserForm(ModelForm):
    class Meta:
        model  = User
        fields = ['username', 'email', 'bio','avatar']