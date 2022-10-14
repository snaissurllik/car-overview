from email import message
from django import forms
from django.forms import CharField, ValidationError
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import *


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Not selected"

    class Meta:
        model = Car
        fields = ('title', 'slug', 'content', 'photo', 'category')

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError("Car name contains more than 50 symbols")
        return title


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput()
        }


class EmailSendForm(forms.Form):
    subject = forms.CharField(required=True)
    from_email = forms.EmailField(label="Your email", required=True)
    message = forms.CharField(label="Your message", widget=forms.Textarea, required=True)


    def send_email(self):
        subject = self.cleaned_data['subject']
        from_email = self.cleaned_data['from_email']
        message = self.cleaned_data['message']
        send_mail(subject, message,
                  from_email, recipient_list=['artyrchir1@gmail.com'])