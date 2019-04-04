import pygame

class Button():
	"""play按钮类"""
	def __init__(self,ai_settings,screen,msg):
		# 初始化信息
		self.ai_settings = ai_settings
		self.screen = screen
		self.screen_rect = self.screen.get_rect()

		# 定义按钮基础信息
		self.button_width = 200
		self.button_height = 50
		self.button_color = (43,43,43)
		self.text_color = (255,255,255)
		self.font = pygame.font.SysFont(None,48)
		# 绘制矩形并居中
		self.rect = pygame.Rect(0,0,self.button_width,self.button_height)
		self.rect.center = self.screen_rect.center

		# 渲染文字为图片
		self.prep_msg(msg)

	def prep_msg(self,msg):
		self.image_msg = self.font.render(msg,True,self.text_color,self.button_color)
		self.image_msg_rect = self.image_msg.get_rect()
		self.image_msg_rect.center = self.screen_rect.center

	def draw_button(self):
		self.screen.fill(self.button_color,self.rect)
		self.screen.blit(self.image_msg,self.image_msg_rect)