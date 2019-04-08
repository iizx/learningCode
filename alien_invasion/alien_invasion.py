
import pygame
from settings import Settings
from ship import Ship
import game_function as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard as sb

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
	# 游戏信息初始化
	stats = GameStats(ai_settings)
	# 分数初始化
	score = sb(ai_settings,screen,stats)
	# 创建开始按钮
	play_button = Button(ai_settings,screen,"Play")
	# 创建外星人群
	gf.create_aliens(screen, ai_settings, aliens, ship)
	# 开始游戏循环
	while True:

		# 监视键盘和鼠标事件
		gf.check_event(screen,ship,ai_settings,bullets,stats,play_button,aliens,score)
		gf.check_high_score(stats,score)
		if stats.game_active:
			ship.update()
			gf.update_bullet(bullets,aliens,screen,ai_settings,ship,stats,score)
			gf.update_aliens(aliens,ai_settings,ship,bullets,screen,stats,score)
		gf.update_screen(ai_settings,screen,ship,bullets,aliens,play_button,stats,score)

run_game()