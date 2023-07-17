from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages

from ..forms import QuestionForm
from ..models import Question


@login_required(login_url='common:login')
def question_create(request):
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():  # 폼이 유효하다면
			question = form.save(commit=False)  # 임시저장하여 question객체를 리턴받는다?
			question.author = request.user
			question.create_date = timezone.now()  # 실제 저장을 위해 작성일시 생성
			question.save()  # 실제 저장
			return redirect('pybo:index')
	else:
		form = QuestionForm()
	context = {'form': form}
	# {'form': form} 은 탬플릿에서 질문 등록시 사용할 폼 엘리먼트를 생성할 때 쓰임
	return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	if request.user != question.author:
		messages.error(request, '수정권한이 없습니다')
		return redirect('pybo:detail', question_id=question.id)
	if request.method == 'POST':
		form = QuestionForm(request.POST, instance=question)
		if form.is_valid():
			question = form.save(commit=False)
			question.modify_date = timezone.now()
			question.save()
			return redirect('pybo:detail', question_id=question.id)
	else:
		form = QuestionForm(instance=question)
	context = {'form': form}
	return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	if request.user != question.author:
		messages.error(request, '삭제권한이 없습니다')
		return redirect('pybo:detail', question_id=question.id)
	question.delete()
	return redirect('pybo:index')


@login_required(login_url='common:login')
def question_vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	if request.user == question.author:
		messages.error(request, '본인이 작성한 글은 추천할 수 없습니다.')
	else:
		question.voter.add(request.user)
	return redirect('pybo:detail', question_id=question.id)


