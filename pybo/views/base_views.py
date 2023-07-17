from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from ..models import Question


def index(request):
	question_list = Question.objects.order_by('-create_date')
	# http://localhost:8000/pybo/?page=1 디폴트 1
	page = request.GET.get('page', '1')  # 페이지
	paginator = Paginator(question_list, 10)  # 페이지당 10개씩
	page_obj = paginator.get_page(page)
	page_end_number = 0
	for end in paginator.page_range:
		page_end_number += 1
	context = {'question_list': page_obj, 'page_end_number': page_end_number,}
	return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	context = {'question': question}
	return render(request, 'pybo/question_detail.html', context)



class IndexView(ListView):
	# template_name = question_list.html # 디폴트: 모델명_list.html
	def get_queryset(self):
		return Question.objects.order_by('-create_date')


# class DetailView(DetailView):
# 	model = Question
# 	# template_name = question_detail.html 디폴트: 모델명_detail.html

