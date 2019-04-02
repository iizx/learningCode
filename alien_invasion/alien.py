from pygame.sprite import Sprite
import pygame

class Alien(Sprite):
	"""关于外星人的类"""
	def __init__(self,screen,ai_settigs):
		# 初始化
		super().__init__()
		self.screen = screen
		self.ai_settings = ai_settigs
		# 获取图片外接矩形
		self.image = pygame.image.load('./images/alien.bmp')
		self.rect = self.image.get_rect()
		# 设置外星人位置
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		# 以小数存储位置
		self.x = float(self.rect.x)
	def check_edges(self):
		# 检测是否触碰边缘
		if self.rect.right >= self.screen.get_rect().right:
			return True
		elif self.rect.left <= 0:
			return True
	def update(self):
		self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
		self.rect.x = self.x