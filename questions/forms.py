from django import forms
from questions.models import Question


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput()
    )


class RegisterForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput
    )
    nickname = forms.CharField(
        required=True
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
    )
    repeat_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
    )
    avatar = forms.FileField(
        allow_empty_file=False,
        widget=forms.FileInput,
        required=False
    )


class EditForm(forms.Form):
    nickname = forms.CharField()
    email = forms.EmailField(
        widget=forms.EmailInput
    )
    avatar = forms.FileField(
        allow_empty_file=False,
        widget=forms.FileInput,
        required=False
    )


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text']

    def __init__(self, author, *args, **kwargs):
        self.author = author
        super().__init__(args, kwargs)

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.author = self.author
        if commit:
            obj.save()
        return obj
