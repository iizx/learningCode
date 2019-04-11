"""定义learning_logs的URL模式"""
from django.urls import path
from . import views

urlpatterns = [
	# 主页
	path(r'',views.index,name='index'),
	# 所有主题信息
	path(r'topics/',views.topics,name='topics'),
	# 特定主题的详细页面
	path(r"topics/<topic_id>/", views.topic, name='topic'),
	# 创建新的主题
	path(r'new_topic/',views.new_topic,name='new_topic'),
	# 创建新的条目
	path(r'new_entry/<topic_id>/',views.new_entry,name='new_entry'),
	# 让用户编辑条目
	path(r'edit_entry/<entry_id>',views.edit_entry,name='edit_entry')
]