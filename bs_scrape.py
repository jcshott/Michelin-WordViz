from models import connect_to_db, db, Reviews, Restaurants
from runserver import app
from datetime import datetime
import os, random, re, time, urllib2

from bs4 import BeautifulSoup

def grab_review_objects(search_url, restaurant_name):
    """
        Grabs all reviews from given restaurant's yelp page.

    """

    rest_time = random.randint(5000, 60000)/1000.0 # before scraping the page, script will rest for between 5 to 60 secs
    print "rest time is", rest_time # print statements to see scraping progress
    time.sleep(rest_time)
    print "url is now", search_url

    contents = urllib2.urlopen(search_url).read()
    soup = BeautifulSoup(contents, "html.parser")

    biz_id = soup.find('a', attrs={'class':'edit-category', 'href':True}).attrs['href'] # grab the yelp biz id
    biz_id = biz_id.replace("/biz_attribute?biz_id=", "") # lop off the prefix
    
    if not restaurant_info: # only need to grab this stuff the first time through review scraping
        restaurant_info['biz_id'] = biz_id
        name = (soup.find('h1', attrs={'itemprop':'name'}).get_text()).strip()
        restaurant_info['name'] = name
        restaurant_info['yelp_name'] = restaurant_name
        restaurant_info["avg_rating"] = float(soup.find('meta', {'itemprop':'ratingValue', 'content':True}).attrs['content'])
        restaurant_info["location"] = soup.find('span', attrs={'itemprop':'addressLocality'}).get_text() + ", " + soup.find('span', attrs={'itemprop':'addressRegion'}).get_text()
        restaurant_info["stars"] = 3
        load_restaurant_info_to_db(restaurant_info)

    next = soup.find('a', attrs={'class':'next'}) # look for the "next" page link
    
    review_objs_list = []
    for review in soup.findAll('div', class_='review') :
        review_objs_list.append(review)

    review_objs_list = review_objs_list[1:] # first item is dummy
    next_page_reviews = []

    if next:
        next_page_reviews, _ = grab_review_objects(next.attrs['href'], restaurant_name)

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

    for review in review_objs_list:
        
        review_id = review.attrs['data-review-id']
        date = review.find('meta', attrs={'itemprop':'datePublished', 'content':True}).attrs['content']
        date = datetime.strptime(date, "%Y-%m-%d")
        rating = float(review.find('meta', {'itemprop':'ratingValue', 'content':True}).attrs['content'])
        location = review.find('li', attrs={'class':'user-location'}).get_text().replace("\n","")
        text = re.sub(ur'\u00a0','',review.find('p', attrs={'itemprop':'description'}).get_text(),re.UNICODE) # get rid of unicode
        r_obj = Restaurants.query.filter_by(biz_id=biz_id).first()
        r_name = r_obj.common_name
        temp_review_obj = Reviews(review_id=review_id, restaurant_name=r_name, biz_id=biz_id, rating=rating, text=text, location=location, date=date)
        db.session.add(temp_review_obj)
    db.session.commit()
    print "reviews added!"

def main(restaurant):
    load_reviews_to_db(restaurant)


if __name__ == "__main__":
    
    connect_to_db(app)

    # needed to construct URLs for scraping
    search_base_url = "https://www.yelp.com/biz/"
    search_suffix = "?sort_by=date_desc"
    starting_url = "https://www.yelp.com"
    restaurant_info = {}
    # the 3 star, US Michelin restaurants to gather data from yelp & dump to db
    restaurant_list = ["jean-georges-new-york", "chefs-table-at-brooklyn-fare-brooklyn-3", "per-se-new-york", "masa-new-york", "alinea-chicago", "grace-chicago-3", ""]

    for item in restaurant_list:
        restaurant_info = {} #clear the restaurant info dict for each new restaurant scraped
        main(item)
