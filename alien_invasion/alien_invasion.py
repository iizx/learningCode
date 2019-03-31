import sys
import pygame
from settings import Settings
from ship import Ship
import game_function as gf

def run_game():
	# 初始化游戏
	pygame.init()
	# 实例化设置类
	ai_settings = Settings()
	# 创建屏幕
	screen = pygame.display.set_mode((ai_settings.scrren_width,ai_settings.scrren_hgiht))
	# 设置游戏名
	pygame.display.set_caption("Aliens Invasion")
	# 设置背景色
	# bg_color = ai_settings.bg_color
	# 实例化飞船类
	ship = Ship(screen,ai_settings)
	# 开始游戏循环
	while True:

		# 监视键盘和鼠标事件
		gf.check_event(ship)
		ship.update()
		gf.update_screen(ai_settings,screen,ship)

run_game()