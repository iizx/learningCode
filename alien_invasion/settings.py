class Settings():
	"""存储外星人入侵游戏的所有设置类"""
	def __init__(self):
		"""初始化游戏设置"""
		# 屏幕设置
		self.scrren_width = 800
		self.scrren_hgiht = 600
		self.bg_color = (230,230,230)
		# 设置飞船初始速度
		self.ship_speed_factor = 1.5