from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from .models import Post


class UserRegistration(UserCreationForm):
    email = forms.EmailField(max_length=250, help_text="The email field is required.")
    first_name = forms.CharField(max_length=250, help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250, help_text="The Last Name field is required.")

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} mail is already exists/taken")


class SavePost(forms.ModelForm):
    user = forms.IntegerField(help_text="User Field is required.")
    title = forms.CharField(max_length=250, help_text="Title Field is required.")
    description = forms.Textarea()

    class Meta:
        model = Post
        fields = ('user', 'title', 'description', 'file_path')

    def clean_title(self):
        id = self.instance.id if not self.instance == None else 0
        try:
            if id.isnumeric():
                post = Post.objects.exclude(id=id).get(title=self.cleaned_data['title'])
            else:
                post = Post.objects.get(title=self.cleaned_data['title'])
        except:
            return self.cleaned_data['title']
        raise forms.ValidationError(f'{post.title} post Already Exists.')

    def clean_user(self):
        user_id = self.cleaned_data['user']
        print("USER: " + str(user_id))
        try:
            user = User.objects.get(id=user_id)
            return user
        except:
            raise forms.ValidationError("User ID is unrecognize.")
