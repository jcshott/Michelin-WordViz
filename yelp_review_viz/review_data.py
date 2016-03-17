class ReviewData(object):
	""" class for review data that will be sent to client for visualization"""

	def __init__(self, restaurant_name):
		
		self.restaurant = restaurant_name
		self.review_words = None

	def function(self):
		""" define the methods here that will return self.review_words as a 
		list of dictionaries (to be jsonified)
		
		"""
		pass
