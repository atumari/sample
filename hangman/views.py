from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from . models import Author, Question
from .forms import AuthorForm, QuestionForm, VoteForm, AnswerForm, AuthorRegisterForm

from . import play_func as pf
import random
import re


# Create your views here.
def index(request):
    params = {
        'title': 'HangMan',
    }
    return render(request, 'hangman/index.html', params)


def play(request):
    if request.method == 'POST':
        answerform = AnswerForm(request.POST)
        ans = request.POST['answer'].lower()
        status = int(request.POST['status'])
        correct = request.POST['correct']
        past_answers = request.POST['past_answers']

        if re.match('[a-z]', ans) and len(ans) == 1:
            if ans not in past_answers:
                past_answers += ans

            if ans not in correct:
                status += 1
        
            msg = ''

        else:
            msg = "答えはアルファベット1文字で入力してください"

        string, score = pf.get_score(past_answers, correct)
        hangman = pf.draw_hangman(status)
      
    else:
        q_num = Question.objects.count()
        rand_idx = random.randint(0, q_num-1) + 1
        correct = Question.objects.get(id=rand_idx).correct
        status = 0
        past_answers = ''
        string, score = pf.get_score(past_answers, correct)
        hangman = pf.draw_hangman(0)
        answerform = AnswerForm(initial = {'correct': correct,
                                            'question_id': rand_idx})
        msg=''

    params = {
        'msg': msg,
        'status': status,
        'past_answers': past_answers,
        'string': string,
        'hangman': hangman,
        'form': answerform, 
    }

    if score == len(correct):
        # 正解の時の処理
        voteform = VoteForm()
        params['voteform'] = voteform
        return render(request, 'hangman/success.html', params)
        
    if status > 5:
        # ゲームオーバーの処理
        return render(request, 'hangman/game_over.html', params)

    return render(request, 'hangman/play.html', params)

def vote(request):
    id = request.POST['question_id']
    question = Question.objects.get(id=id)

    #if request.POST['vote'] and not 'voted' in request.session:
    if 'vote' in request.POST:
        #request.session['voted'] = True
        question.point += 1
        author = question.author
        author.point += 1
        question.save()
        author.save()

    return redirect(to='index')


def admin(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        name = request.POST['name']
        author = Author.objects.filter(name=name).first()

        if author and author.password == request.POST['password']:
            params = {
                'authorform': form,
                'questionform': QuestionForm(),
            }
            return render(request, 'hangman/create.html', params)
        else:
            msg = '名前とパスワードが一致しません。'

    else:
        form = AuthorForm()
        msg = ''

    params = {
        'form': form,
        'msg': msg,
    }

    return render(request, 'hangman/admin.html', params)

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        check_auth = Author.objects.filter(name=name).first()

        if check_auth:
            # すでに同名のAuthorがいる場合
            msg = 'その名前は既に使われています。'

        else:
            obj = Author()
            author = AuthorForm(request.POST, instance=obj)
            author.save()
            params = {
                "form": author,
            }
            return render(request, 'hangman/complete.html', params)

    else:
        msg = ''

    params = {
        'form': AuthorForm(),
        'msg': msg
        }

    return render(request, 'hangman/register.html', params)

def create(request):
    authorform = AuthorForm(request.POST)
    questionform = QuestionForm(request.POST)
    correct = request.POST['correct'].lower()
    params = {
        'authorform': authorform,
        'questionform': questionform,
        'msg': None,
    }

    if len(correct) >= 5 and len(correct) <= 10 and not(re.match('[^a-z]', correct)):
        name = request.POST['name']
        if Question.objects.filter(correct=correct).first():
            params['msg'] = "その問題は既に作られています。"
        else:
            params['msg'] = "登録が完了しました。"
            author = Author.objects.filter(name=name).first()
            question = Question()
            question.author = author
            question.correct = correct
            question.save()
            author.num_questions += 1
            author.save()
        return render(request, 'hangman/create_complete.html', params)
    
    else:
        msg = '不正な入力です。'
        params['msg'] = msg
    return render(request, 'hangman/create.html', params)

def ranking(request, num=1):
    authors = Author.objects.all().order_by("point").reverse()
    page = Paginator(authors, 10)
    params = {
        'authors': page.get_page(num),
        'page_rank': (num - 1) * 10
    }
    return render(request, 'hangman/ranking.html', params)
