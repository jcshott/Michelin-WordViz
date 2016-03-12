from scrapy.spider import BaseSpider

from yelp_app.items import YelpReview

class YelpSpider(BaseSpider, restaurant_id):
    """Spider for yelp reviews"""
    name = "yelp_spider"
    allowed_domains = ["yelp.com"]
    start_urls = ["https://www.yelp.com/biz/" + restaurant_id]

    deals_list_xpath = '//div[@class="review review--with-sidebar"]'
    item_fields = {
        'yelp_review_id': './/@data-review-id',
        'text': './/div[@class="review-wrapper"]/div[@class="review-content"]/p[@itemprop="description"]',
        'rating': './/div[@class="review-wrapper"]/div[@class="review-content"]/div[@class="biz-rating biz-rating-very-large clearfix"]/div[@itemprop="reviewRating"]/div[@class="rating-very-large"]/meta/@content',
        'date': './/div[@class="review-wrapper"]/div[@class="review-content"]/div[@class="biz-rating biz-rating-very-large clearfix"]/span[@class="rating-qualifier"]/meta/@content]',
        'reviewer_location': './/div[@class="review-sidebar"]/div[@class="review-sidebar-content"]/div[@class="ypassport media-block"]/div[@class="media-story"]/ul[@class="user-passport-info"]/li[@class="user-location"]/text()',
        'restraunt_id': restaurant_id
    }
