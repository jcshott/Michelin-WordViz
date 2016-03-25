from models import connect_to_db, db, Reviews, Restaurants
from runserver import app
import os
import random
import re
import time
import urllib2

from bs4 import BeautifulSoup

## TODO: Add restaurant to db in the grab-review-obj fn. add reviews to db in dump reviews fn

def grab_review_objects(search_url, restaurant_name):
    """
        Grabs all reviews from given restaurant's yelp page.

    """
    restaurant_info = {}

    rest_time = random.randint(5000, 60000)/1000.0 # before scraping the page, script will rest for between 5 to 60 secs
    print "rest time is", rest_time # print statements to see scraping progress
    time.sleep(rest_time)
    print "url is now", search_url

    contents = urllib2.urlopen(search_url).read()
    soup = BeautifulSoup(contents, "html.parser")

    if not restaurant_info: # only need to grab this stuff the first time through review scraping
        biz_id = soup.find('a', attrs={'class':'edit-category', 'href':True}).attrs['href'] # grab the yelp biz id
        restaurant_info['biz_id'] = biz_id.replace("/biz_attribute?biz_id=", "") # lop off the prefix
        restaurant_info['name'] = (soup.find('h1', attrs={'itemprop':'name'}).get_text()).strip()
        restaurant_info['yelp_name'] = restaurant_name
        restaurant_info["avg_rating"] = float(soup.find('meta', {'itemprop':'ratingValue', 'content':True}).attrs['content'])
        restaurant_info["location"] = soup.find('span', attrs={'itemprop':'addressLocality'}).get_text() + ", " + soup.find('span', attrs={'itemprop':'addressRegion'}).get_text()
        restaurant_info["stars"] = 3

    next = soup.find('a', attrs={'class':'next'}) # look for the "next" page link
    
    review_objs_list = []
    for review in soup.findAll('div', class_='review') :
        review_objs_list.append(review)

    review_objs_list = review_objs_list[1:] # first item is dummy
    next_page_reviews = []

    if next:
        next_page_reviews, _ = grab_review_objects(next.attrs['href'], restaurant_name)

    
    load_restaurant_info_to_db(restaurant_info)
    
    return review_objs_list + next_page_reviews, biz_id

def load_restaurant_info_to_db(restaurant_info):

    biz_id = restaurant_info["biz_id"]
    name = restaurant_info["name"]
    yelp_name = restaurant_info["yelp_name"]
    avg_rating = float(restaurant_info["avg_rating"])
    location = restaurant_info["location"]
    stars = int(restaurant_info["stars"])

    temp_rest_obj = Restaurants(biz_id=biz_id, common_name=name, yelp_name=yelp_name, location=location, avg_yelp_rating=avg_rating, michelin_stars=stars)

    db.session.add(temp_rest_obj)
    db.session.commit()
    print "restaurant info added!"


def load_reviews_to_db(restaurant):

    search_url = search_base_url + restaurant + search_suffix
    review_objs_list, biz_id = grab_review_objects(search_url, restaurant)
    review_dicts_20 = []
    for review in review_objs_list:
        
        review_dict['review_id'] = review.attrs['data-review-id']
        review_dict['date'] = review.find('meta', attrs={'itemprop':'datePublished', 'content':True}).attrs['content']
        review_dict['rating'] = float(review.find('meta', {'itemprop':'ratingValue', 'content':True}).attrs['content'])
        review_dict['location'] = review.find('li', attrs={'class':'user-location'}).get_text().replace("\n","")
        review_dict['restaurant'] = restaurant
        review_dict['text'] = re.sub(ur'\u00a0','',review.find('p', attrs={'itemprop':'description'}).get_text(),re.UNICODE) # get rid of unicode
        review_dict['biz_id'] = biz_id # primary key in restaurants table, foreign key in reviews table
        review_dicts_20.append(review_dict)


def main(restaurant):
    load_reviews_to_db(restaurant)


if __name__ == "__main__":
    
    connect_to_db(app)

    # needed to construct URLs for scraping
    search_base_url = "https://www.yelp.com/biz/"
    search_suffix = "?sort_by=date_desc"
    starting_url = "https://www.yelp.com"
    
    # the 3 star, US Michelin restaurants to gather data from yelp & dump to db
    restaurant_list = ["jean-georges-new-york", "chefs-table-at-brooklyn-fare-brooklyn-3", "per-se-new-york", "masa-new-york"]

    for item in restaurant_list:
        main(item)
