import logging

from django import forms
from django.contrib import auth
from questions.models import Question, Tag, Answer, User, Profile

logger = logging.getLogger(__name__)


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.request = kwargs.pop('request', None)
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        cdata = self.cleaned_data
        user = auth.authenticate(
            username=cdata['username'],
            password=cdata['password']
        )
        if user is None:
            logger.debug('Wrong username or password')
            raise forms.ValidationError('Wrong username or password')
        auth.login(self.request, user)


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
        widget=forms.ClearableFileInput,
        required=False
    )

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar is None:
            return None
        if 'image' not in avatar.content_type:
            logger.debug('Invalid file type')
            raise forms.ValidationError('Invalid file type')
        return avatar

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if email == "":
            return email
        if email.find('@') < 1 or len(email) < 3:
            logger.debug('Invalid email')
            raise forms.ValidationError('Invalid email')
        try:
            _ = User.objects.get(email=email)
            logger.debug('User already exists')
            raise forms.ValidationError('User with the same email is exist')
        except User.DoesNotExist:
            return email

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname', '')
        if len(nickname) > 30:
            logger.debug('Too long nickname')
            raise forms.ValidationError(
                'Nickname is to be less than 30 symbols')
        if len(nickname) < 6:
            logger.debug('Too short nickname')
            raise forms.ValidationError('Nickname is to be more than 5 symbols')
        try:
            _ = User.objects.get(username=nickname)
            logger.debug('User already exists')
            raise forms.ValidationError('User with the same nickname is exist')
        except User.DoesNotExist:
            return nickname

    def clean_password(self):
        password = self.cleaned_data.get('password', '')
        if len(password) < 6:
            raise forms.ValidationError('Password is to be more than 5 symbols')
        return password

    def clean_repeat_password(self):
        repeat_password = self.cleaned_data.get('repeat_password', '')
        password = self.cleaned_data.get('password', '')
        if repeat_password != password:
            raise forms.ValidationError('Field isn\'t equal to password')
        return repeat_password

    def save(self, request):
        logger.info('Creating new user')
        cdata = self.cleaned_data
        user = User.objects.create_user(
            cdata['nickname'],
            cdata['email'],
            cdata['password']
        )
        user.save()
        profile = Profile.objects.create(user=user, nickname=cdata['nickname'])
        if 'avatar' in cdata and cdata['avatar'] is not None:
            profile.avatar = request.FILES['avatar']
        profile.save()


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
        widget=forms.ClearableFileInput,
        required=False
    )

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if email == '':
            return email
        if email.find('@') < 1 or len(email) < 3:
            raise forms.ValidationError('Wrong email')
        try:
            _ = User.objects.get(email=email)
            raise forms.ValidationError('User with the same email is exist')
        except User.DoesNotExist:
            return email

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname', '')
        if nickname == '':
            return nickname
        if len(nickname) > 30:
            raise forms.ValidationError(
                'Nickname is to be less than 30 symbols')
        if len(nickname) < 6:
            raise forms.ValidationError('Nickname is to be more than 5 symbols')
        try:
            _ = User.objects.get(username=nickname)
            raise forms.ValidationError('User with the same nickname is exist')
        except User.DoesNotExist:
            return nickname

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar', None)
        if avatar is not None and 'image' not in avatar.content_type:
            raise forms.ValidationError('Invalid type of file')
        return avatar

    def clean(self):
        cleaned_data = super().clean()
        if not self.is_valid():
            return cleaned_data

        if cleaned_data['email'] == '' and cleaned_data['nickname'] == '' \
                and cleaned_data['avatar'] is not None:
            msg = 'You need to feel at least one field'
            self.add_error('nickname', msg)
            self.add_error('email', msg)
            raise forms.ValidationError(msg, code='empty')

        return cleaned_data

    def save(self, request):
        logger.info('Updating user')
        cdata = self.cleaned_data
        user = auth.get_user(request)
        profile = Profile.objects.get(user=user)
        if 'nickname' in cdata and cdata['nickname'] != '':
            user.username = cdata['nickname']
            profile.nickname = cdata['nickname']
        if 'email' in cdata and cdata['email'] != '':
            user.email = cdata['email']
        if 'avatar' in cdata and cdata['avatar'] is not None:
            profile.avatar = request.FILES['avatar']
        profile.save()
        user.save()


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

    def clean_text(self):
        text = self.cleaned_data.get('text', '')
        if len(text.strip()) == 0:
            raise forms.ValidationError("Text of question is to be not empty")
        return text

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        if len(title.strip()) == 0:
            raise forms.ValidationError("Title is to be not empty")
        return title

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        tag_list = tags.split()
        if len(tag_list) == 0:
            raise forms.ValidationError("Tags are to be not empty")
        for tag in tags:
            if not tag.isalpha():
                raise forms.ValidationError("You can use only letters in tags")

        return tags

    def save(self, user):
        logger.info('Creating new question')
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

    def clean_text(self):
        text = self.cleaned_data.get('text', '')
        if len(text.strip()) == 0:
            raise forms.ValidationError("Text of question is to be not empty")
        return text

    def save(self, user, question):
        logger.info('Creating new answer')
        answer = Answer.objects.create(
            text=self.data['text'],
            author=user,
            question=question
        )
        answer.save()
