"""定义learning_logs的URL模式"""
from django.urls import path
from . import views

urlpatterns = [
	# 主页
	path(r'',views.index,name='index'),
	# 所有主题信息
	path(r'topics/',views.topics,name='topics'),
	# 特定主题的详细页面
	path(r"topics/<topic_id>/", views.topic, name='topic')

]