class GameStats():
	"""跟踪游戏的统计信息"""
	def __init__(self,ai_settings):
		"""初始化统计信息"""
		self.ai_settings = ai_settings
		self.game_active = True
		self.reset_stats()

	def reset_stats(self):
		self.left_ship = self.ai_settings.ship_limit