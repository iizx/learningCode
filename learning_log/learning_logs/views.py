from django.shortcuts import render
from .models import Topic
# Create your views here.
def index(request):
	"""学习笔记主页"""
	return render(request,'learning_logs/index.html')

def topics(request):
	"""返回所有主题信息"""
	topics = Topic.objects.order_by('date_add')
	context = {'topics':topics}
	return render(request,'learning_logs/topics.html',context)
def topic(request,topic_id):
	"""特定主题的详细页面"""
	topic = Topic.objects.get(id=topic_id)
	entries = topic.entry_set.order_by('-date_add')
	context = {'topic':topic,'entries':entries}
	return render(request, 'learning_logs/topic.html', context)
