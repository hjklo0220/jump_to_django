from django import forms
from pybo.models import Question, Answer


# forms.ModelForm은 모델(Model)과 연결된 폼으로 폼을 저장하면 연결된 모델의 데이터를 저장할수 있는 폼
class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question  # 사용할 모델
		fields = ['subject', 'content']  # QuestionForm에서 사용할 Question모델의 속성
		# widgets속성을 지정하여 부트스트랩 클래스 추가 가능
		# widgets = {
		# 	'subject': forms.TextInput(attrs={'class': 'form-control'}),
		# 	'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10})
		# }
		# 한글로 표시
		labels = {
			'subject': '제목',
			'content': '내용',
		}

class AnswerForm(forms.ModelForm):
	class Meta:
		model = Answer
		fields = ['content']
		labels = {
			'content': "답변내용"
		}


