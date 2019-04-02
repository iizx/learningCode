import sys
import pygame
from bullet import Bullet
from alien import Alien

def check_keydowm_event(event,screen,ship,ai_setting,bullets):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		if len(bullets) < ai_setting.bullets_allowed:
			new_bullet = Bullet(screen,ship,ai_setting)
			bullets.add(new_bullet)
	elif event.key == pygame.K_q:
		sys.exit()

def check_keyup_event(event,ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False

def check_event(screen,ship,ai_setting,bullets):
	"""响应按键和鼠标事件"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydowm_event(event,screen,ship,ai_setting,bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_event(event,ship)

def update_screen(ai_settings,screen,ship,bullets,aliens):
	"""更新屏幕并切换图像"""
	# 循环时重绘屏幕
	screen.fill(ai_settings.bg_color)
	ship.blitme()
	for bullet in bullets:
		bullet.draw_bullet()
	aliens.draw(screen)
	# 让新绘制的屏幕可见
	pygame.display.flip()

def del_bullet(bullets):
	"""删除已经消失的子弹"""
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

def create_aliens(screen,ai_settings,aliens,ship):
	"""创建外星人群"""
	# 计算横向空间
	new_alien = Alien(screen,ai_settings)
	alien_width = new_alien.rect.width
	invailable_x = ai_settings.screen_width - 2 * alien_width
	# 计算纵向空间
	alien_height = new_alien.rect.height
	invailable_y = ai_settings.screen_height - 2 * alien_height - ship.rect.height
	# 分母加括号
	invailable_num_x = int(invailable_x / (2 * alien_width) )
	invailable_num_y = int(invailable_y / (2 * alien_height))
	for num_y in range(invailable_num_y):
		for num_x in range(invailable_num_x):
			alien = Alien(screen,ai_settings)
			# 重设x坐标，放置在一行
			alien.x = alien.rect.width + 2 * alien_width * num_x
			alien.rect.x = alien.x
			# 重设y坐标
			alien.rect.y = alien.rect.height + 2 * alien_height * num_y
			aliens.add(alien)
def check_edges(aliens,ai_settings):
	# 边缘碰撞检测
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(aliens,ai_settings)
			break
def change_fleet_direction(aliens,ai_settings):
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
def update_aliens(aliens,ai_settings):
	# 检查边缘碰撞并改变方向
	check_edges(aliens,ai_settings)
	aliens.update()