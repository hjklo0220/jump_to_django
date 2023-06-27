from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from django.utils import timezone
from django.views.generic import ListView, DetailView

from pybo.forms import QuestionForm, AnswerForm
from pybo.models import Question, Answer


# Create your views here.
# def index(request):
# 	question_list = Question.objects.order_by('-create_date')
# 	context = {'question_list': question_list}
# 	return render(request, 'pybo/question_list.html', context)

class IndexView(ListView):
	# template_name = question_list.html # 디폴트: 모델명_list.html
	def get_queryset(self):
		return Question.objects.order_by('-create_date')


def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	context = {'question': question}
	return render(request, 'pybo/question_detail.html', context)

# class DetailView(DetailView):
# 	model = Question
# 	# template_name = question_detail.html 디폴트: 모델명_detail.html

# 답변 등록 로직
def answer_create(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	# question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
	# answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
	# answer.save()
	if request.method == "POST":
		form = AnswerForm(request.POST)
		if form.is_valid():
			answer = form.save(commit=False)
			answer.create_date = timezone.now()
			answer.question = question
			answer.save()
			return redirect('pybo:detail', question_id=question.id)
	else:
		return HttpResponseNotAllowed('Only POST is possible.')
	context = {'question': question, 'form': form}
	return render(request, 'pybo/question_detail.html', context)


def question_create(request):
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():  # 폼이 유효하다면
			question = form.save(commit=False)  # 임시저장하여 question객체를 리턴받는다?
			question.create_date = timezone.now()  # 실제 저장을 위해 작성일시 생성
			question.save()  # 실제 저장
			return redirect('pybo:index')
	else:
		form = QuestionForm()
	context = {'form': form}
	# {'form': form} 은 탬플릿에서 질문 등록시 사용할 폼 엘리먼트를 생성할 때 쓰임
	return render(request, 'pybo/question_form.html', context)



