import pygame
from pygame.sprite import Group
from ship import Ship

class ScoreBoard():
	"""得分相关类"""
	def __init__(self,ai_settings,screen,stats):
		self.stats = stats
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.ai_settings = ai_settings

		# 设置字体/颜色
		self.text_color = (30,30,30)
		self.font = pygame.font.SysFont(None,48)

		# 渲染为图片
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()

	def prep_score(self):
		# 圆整分数
		self.round_score = round(self.stats.score,-1)
		self.score_str = "{:,}".format(self.round_score)
		self.score_img = self.font.render(self.score_str,True,self.text_color,self.ai_settings.bg_color)

		# 放置在屏幕右上角
		self.rect = self.score_img.get_rect()
		self.rect.right = self.screen_rect.right - 20
		self.rect.top = 20
	def prep_high_score(self):
		# 圆整分数
		self.round_high_score = round(self.stats.high_score,-1)
		self.high_score_str = "{:,}".format(self.round_high_score)
		self.high_score_img = self.font.render(self.high_score_str,True,self.text_color,self.ai_settings.bg_color)

		# 放置在屏幕上方中间
		self.high_score_rect = self.high_score_img.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.screen_rect.top

	def prep_level(self):
		self.level_str = str(self.stats.level)
		self.level_img = self.font.render(self.level_str,True,self.text_color,self.ai_settings.bg_color)

		# 放置在分数下方
		self.level_rect = self.level_img.get_rect()
		self.level_rect.right = self.rect.right
		self.level_rect.top = self.rect.bottom + 10


	def prep_ships(self):
		# 飞船编组
		self.ships = Group()
		for ship_number in range(self.stats.left_ship):
			ship = Ship(self.screen,self.ai_settings)
			# 设置位置
			ship.rect.x = 10 + ship_number*ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)

	def show_score(self):
		# 分数展示
		self.screen.blit(self.score_img,self.rect)
		self.screen.blit(self.high_score_img, self.high_score_rect)
		self.screen.blit(self.level_img,self.level_rect)
		self.ships.draw(self.screen)