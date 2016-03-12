from scrapy.item import Item, Field

class YelpReview(Item):
	"""Container (dictionary-like object) for scraped data"""

	yelp_review_id = Field()
	text = Field()
	rating = Field()
	date = Field()
	reviewer_location = Field()
	restraunt_id = Field()

