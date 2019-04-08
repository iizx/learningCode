class Settings():
	"""存储外星人入侵游戏的所有设置类"""
	def __init__(self):
		"""初始化游戏设置"""
		# 屏幕设置
		self.screen_width = 800
		self.screen_height = 600
		self.bg_color = (230,230,230)

		self.ship_limit = 3

		# 子弹设置

		self.bullet_width = 300
		self.bullet_height = 15
		self.bullet_color = (60,60,60)
		self.bullets_allowed = 3

		# 向下移动速度
		self.fleet_drop_speed = 100
		# 游戏节奏控制
		self.speedup_scale = 1.1
		# 动态属性初始化
		self.initialize_dynamic_settings()
		# 分数节奏控制
		self.score_scale = 1.5

	def initialize_dynamic_settings(self):
		# 设置初始速度
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 3
		self.alien_speed_factor = 1
		# 1向右移；-1向左移（方向控制）
		self.fleet_direction = 1
		# 外星人分数
		self.alien_points = 50

	def increase_speed(self):
		"""提高速度设置"""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		self.alien_points = int(self.alien_points * self.score_scale)