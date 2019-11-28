from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django_summernote import fields as summer_fields
from .models import Post, Comment


User = get_user_model()


class PostForm(forms.ModelForm):
    title = forms.CharField(label='제목', widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    # text = forms.CharField(label='내용', widget=forms.Textarea(attrs={'class': 'form-control'}), required=True)
    text = summer_fields.SummernoteTextFormField(label='', widget=forms.TextInput(), error_messages={'required': (u'내용을 입력해주세요'),})

    class Meta:
        model = Post
        fields = ('title', 'text',)


class CommentForm(forms.ModelForm):
    author = forms.CharField(label='닉네임', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm md-2', 'placeholder': '닉네임', 'aria-label': '닉네임'}), required=True)
    text = forms.CharField(label='내용', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '내용', 'aria-label': '내용'}), required=True)
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm', 'placeholder': '비밀번호', 'aria-label': '비밀번호'}), required=True)

    class Meta:
        model = Comment
        fields = ('author', 'text', 'password',)


class CreateUserForm(UserCreationForm):
    username = forms.CharField(label='사용자 이름', widget=forms.TextInput(attrs={'class': 'form-control col-6'}), required=True)
    email = forms.EmailField(label='이메일', widget=forms.EmailInput(attrs={'class': 'form-control col-6'}), required=True)
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput(attrs={'class': 'form-control col-6'}), required=True)
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput(attrs={'class': 'form-control col-6'}), required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    # User.objects.get()


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(label='사용자 이름', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CommentDelete(forms.Form):
    password_confirm = forms.CharField(label='비밀번호', widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password_confirm'}), required=True)
    comment_id = forms.CharField(label='닉네임', widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'author'}), required=True)