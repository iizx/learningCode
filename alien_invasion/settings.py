class Settings():
	"""存储外星人入侵游戏的所有设置类"""
	def __init__(self):
		"""初始化游戏设置"""
		# 屏幕设置
		self.screen_width = 800
		self.screen_height = 600
		self.bg_color = (230,230,230)
		# 设置飞船初始速度
		self.ship_speed_factor = 1.5

		# 子弹设置
		self.bullet_speed_factor = 1
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60,60,60)
		self.bullets_allowed = 3
		# 外星人设置
		self.alien_speed_factor = 1
		# 向下移动速度
		self.fleet_drop_speed = 10
		# 1向右移；-1向左移
		self.fleet_direction = 1