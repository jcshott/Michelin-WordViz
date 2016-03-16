# -*- coding: utf-8 -*-

# Scrapy settings for yelp project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'yelp_spider'

SPIDER_MODULES = ['yelp_app.spiders']
NEWSPIDER_MODULE = 'yelp_app.spiders'
ITEM_PIPELINES = ['yelp_app.pipelines.YelpReviewPipeline']

DATABASE = {
	'drivername': 'postgres',
	'host': 'localhost',
	'port': '5432',
	'username': 'yelpproject',
	'password': '',
	'database': 'yelpreviewviz'
}