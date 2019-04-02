import pygame
from pygame.sprite import Sprite
class Bullet(Sprite):
	"""一个子弹类"""
	def __init__(self,screen,ship,ai_setting):
		# 调用父类初始函数初始化自身
		super().__init__()
		self.screen = screen
		# 绘制子弹
		self.rect = pygame.Rect(0, 0, ai_setting.bullet_width ,ai_setting.bullet_height)
		# 重设位置
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top
		# 储存小数表示的子弹位置
		self.y = float(self.rect.y)

		self.color = ai_setting.bullet_color
		self.speed = ai_setting.bullet_speed_factor

	def update(self):
		"""向上移动子弹"""
		self.y -= self.speed
		self.rect.y = self.y

	def draw_bullet(self):
		"""在屏幕上绘制子弹"""
		pygame.draw.rect(self.screen,self.color,self.rect)