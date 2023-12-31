from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
# from django.views.generic import ListView, DetailView

from ..models import Question
import logging


# 로거 객체 생성
logger = logging.getLogger('pybo')


def index(request):
	logger.info("INFO 레벨로 출력")
	page = request.GET.get('page', '1')  # 페이지 http://localhost:8000/pybo/?page=1 디폴트 1
	question_list = Question.objects.order_by('-create_date')
	kw = request.GET.get('kw', '')  # 검색어
	if kw:
		question_list = question_list.filter(
			Q(subject__icontains=kw) |  # 제목 검색
			Q(content__icontains=kw) |  # 내용 검색
			Q(answer__content__icontains=kw) |  # 답변 내용 검색
			Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
			Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
		).distinct()
	paginator = Paginator(question_list, 10)  # 페이지당 10개씩
	page_obj = paginator.get_page(page)
	page_end_number = paginator.num_pages  # 페이지 총 갯수
	context = {
		'question_list': page_obj,
		'page_end_number': page_end_number,
		'page': page,
		'kw': kw,
	}
	return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	context = {'question': question}
	return render(request, 'pybo/question_detail.html', context)



# class IndexView(ListView):
# 	# template_name = question_list.html # 디폴트: 모델명_list.html
# 	def get_queryset(self):
# 		return Question.objects.order_by('-create_date')


# class DetailView(DetailView):
# 	model = Question
# 	# template_name = question_detail.html 디폴트: 모델명_detail.html

