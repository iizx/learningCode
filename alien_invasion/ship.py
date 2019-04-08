import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	"""飞船管理模块"""
	def __init__(self,screen,ai_settings):
		# 导入sprite模块并初始化
		super().__init__()
		"""初始化飞船并设置其初始位置"""
		self.screen = screen
		self.ai_settings = ai_settings
		# 加载飞船并获取其外接矩形
		self.image = pygame.transform.scale(pygame.image.load('images/ship.bmp'),(30,24))
		self.rect = self.image.get_rect()
		# 获取屏幕外接矩形
		self.screen_rect = screen.get_rect()


		# 将飞船放置在屏幕中央
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom

		# 在飞船center中存储小数值
		self.center = float(self.rect.centerx)
		# 飞船移动标志位
		self.moving_right = False
		self.moving_left = False

	def update(self):
		"""控制飞船移动"""
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed_factor
		# 根据center更新rect对象
		self.rect.centerx = self.center

		# 绘制飞船
	def blitme(self):
		"""在指定位置绘制飞船"""
		self.screen.blit(self.image,self.rect)

		# 飞船居中
	def center_ship(self):
		self.center = self.screen_rect.centerx