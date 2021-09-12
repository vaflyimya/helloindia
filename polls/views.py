from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic

from django.template import loader

from .models import Choice, Question, Comment
from .forms import CommentForm


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

class CommentDetailView(generic.DetailView):
    model = Comment
    template_name = 'polls/onecomm.html'
    context_object_name = 'comm'

def comments(request):
    latest_comment_list = Comment.objects.all()
    return render(request, 'polls/comments.html', {'latest_comment_list': latest_comment_list})

def combo(request):
    error = ''
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('http://vaflyimya.pythonanywhere.com/polls/combo/')
        else:
            error = 'в глаза долбишься, чушок? заполни нормально'

    form = CommentForm()
    context = {
        'form': form,
        'latest_comment_list': Comment.objects.all()
    }
    return render(request, 'polls/combo.html', context)

def create(request):
    error = ''
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('http://127.0.0.1:8000/polls/comments/')
        else:
            error = 'в глаза долбишься, чушок? заполни нормально'

    form = CommentForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'polls/addcomm.html', data)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
