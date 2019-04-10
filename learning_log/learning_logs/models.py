from django.db import models

# Create your models here.
class Topic(models.Model):
	"""用户学习的主题"""
	text = models.CharField(max_length=200)
	date_add = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		"""返回模型的字符串表示"""
		return self.text

class Entry(models.Model):
	"""学到的关于某个主题的知识"""
	topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
	text = models.TextField()
	date_add = models.DateTimeField(auto_now_add=True)

	class Mate:
		verbose_name_plural = "entries"

	def __str__(self):
		"""返回模型的字符串表示"""
		return self.text[:50] + '...'