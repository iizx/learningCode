import sys
import pygame
from settings import Settings
from ship import Ship
import game_function as gf
from pygame.sprite import Group
from alien import Alien

def run_game():
	# 初始化游戏
	pygame.init()
	# 实例化设置类
	ai_settings = Settings()
	# 创建屏幕
	screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
	# 设置游戏名
	pygame.display.set_caption("Aliens Invasion")
	# 实例化飞船类
	ship = Ship(screen,ai_settings)
	# 实例化外星人
	alien = Alien(screen,ai_settings)
	# 实例化编组
	bullets = Group()
	aliens = Group()
	# 创建外星人群
	gf.create_aliens(screen, ai_settings, aliens, ship)
	# 开始游戏循环
	while True:

		# 监视键盘和鼠标事件
		gf.check_event(screen,ship,ai_settings,bullets)
		ship.update()
		bullets.update()
		# 删除已消失的子弹
		gf.del_bullet(bullets)
		gf.update_aliens(aliens,ai_settings)
		gf.update_screen(ai_settings,screen,ship,bullets,aliens)

run_game()