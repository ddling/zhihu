import ConfigParser

class Utils:

	def __init__(self):
		self.config = ConfigParser.ConfigParser()
		self.config.read('config.ini')

	def get(self, key):
		value = None
		value = self.config.get("info", key)
		return value