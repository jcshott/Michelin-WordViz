from scrapy.spiders import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

from yelp_app.items import YelpReview

class YelpSpider(BaseSpider):
    """Spider for yelp reviews"""
    name = "yelp_spider"
    allowed_domains = ["yelp.com"]
    start_urls = ["https://www.yelp.com/biz/the-french-laundry-yountville-2"]

    reviews_list_xpath = '//div[@class="review review--with-sidebar"]'
    item_fields = {
        'yelp_review_id': './/@data-review-id',
        'text': './/div[@class="review-wrapper"]/div[@class="review-content"]/p[@itemprop="description"]',
        'rating': './/div[@class="review-wrapper"]/div[@class="review-content"]/div[@class="biz-rating biz-rating-very-large clearfix"]/div[@itemprop="reviewRating"]/div[@class="rating-very-large"]/meta/@content',
        'date': './/div[@class="review-wrapper"]/div[@class="review-content"]/div[@class="biz-rating biz-rating-very-large clearfix"]/span[@class="rating-qualifier"]/meta/@content',
        'reviewer_location': './/div[@class="review-sidebar"]/div[@class="review-sidebar-content"]/div[@class="ypassport media-block"]/div[@class="media-story"]/ul[@class="user-passport-info"]/li[@class="user-location"]/b/text()',
    }

    def parse(self, response):

        selector = HtmlXPathSelector(response)

        for review in selector.select(self.reviews_list_xpath):
            loader = XPathItemLoader(YelpReview(), selector=review)

            # define processors
            loader.default_input_processor = MapCompose(unicode.strip)
            loader.default_output_processor = Join()

            # iterate over fields and add xpaths to the loader
            for field, xpath in self.item_fields.iteritems():
                loader.add_xpath(field, xpath)
            yield loader.load_item()