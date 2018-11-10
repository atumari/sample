from django import forms
from .models import Author, Question

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'password']

class QuestionForm(forms.Form):
    correct = forms.CharField(label='問題', max_length=10)

class VoteForm(forms.Form):
    vote = forms.BooleanField(label='投票する', required=False)

class AnswerForm(forms.Form):
    #answer = forms.CharField(label='答え', max_length=1, initial='')
    correct = forms.CharField(label='correct', max_length=10)
    question_id = forms.IntegerField()

class AuthorRegisterForm(forms.Form):
    name = forms.CharField(label='名前', min_length=1, max_length=50)
    password = forms.CharField(label='パスワード', min_length=1, max_length=50)

        