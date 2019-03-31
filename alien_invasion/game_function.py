import sys
import pygame

def check_keydowm_event(event,ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True

def check_keyup_event(event,ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False

def check_event(ship):
	"""响应按键和鼠标事件"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydowm_event(event,ship)
		elif event.type == pygame.KEYUP:
			check_keyup_event(event,ship)

def update_screen(ai_settings,screen,ship):
	"""更新屏幕并切换图像"""
	# 循环时重绘屏幕
	screen.fill(ai_settings.bg_color)
	ship.blitme()
	# 让新绘制的屏幕可见
	pygame.display.flip()