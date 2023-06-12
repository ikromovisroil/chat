from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from .models import *

class Userprofilform(UserChangeForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'readonly': True}))

    class Meta:
        model = User
        fields = ('email','first_name','last_name','image','phone','about',)

    def __init__(self,*args,**kwargs):
        super(Userprofilform,self).__init__(*args,**kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'



class Userloginform(AuthenticationForm):

    class Meta:
        model = User
        fields = ('username','password',)


class Userregisterform(UserCreationForm):

    class Meta:
        model = User
        fields = ('role','first_name','last_name','username','password1','password2',)


class Chatform(forms.ModelForm):

    class Meta:
        model = Chat
        fields = ('user1','content','image',)

