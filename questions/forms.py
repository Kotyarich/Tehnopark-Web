from django import forms
from questions.models import Question, Tag, Answer


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
    nickname = forms.CharField(
        required=False
    )
    email = forms.EmailField(
        widget=forms.EmailInput,
        required=False
    )
    avatar = forms.FileField(
        allow_empty_file=False,
        widget=forms.FileInput,
        required=False
    )


class QuestionForm(forms.Form):
    title = forms.CharField(
        required=True
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 40})
    )
    tags = forms.CharField(
        required=True
    )

    def save(self, user):
        data = self.cleaned_data
        question = Question.objects.create(
            title=data['title'],
            text=data['text'],
            author=user
        )

        tag_lables = data['tags'].split()
        for lable in tag_lables:
            tag, _ = Tag.objects.get_or_create(text=lable)
            question.tags.add(tag)
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 40})
    )

    def save(self, user, question):
        answer = Answer.objects.create(
            text=self.data['text'],
            author=user,
            question=question
        )
        answer.save()

