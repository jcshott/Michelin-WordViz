import json
import os
import random
import re
import time
import urllib2

from bs4 import BeautifulSoup


def grab_review_objects(search_url, restaurant_name):
    rest_time = random.randint(5000, 60000)/1000.0 # before scraping the page, script will rest for between 5 to 60 secs
    print "rest time is", rest_time # print statements to see scraping progress
    time.sleep(rest_time)
    print "url is now", search_url

    contents = urllib2.urlopen(search_url).read()
    soup = BeautifulSoup(contents, "html.parser")
    biz_id = soup.find('a', attrs={'class':'edit-category', 'href':True}).attrs['href'] # grab the yelp biz id
    biz_id = biz_id.replace("/biz_attribute?biz_id=", "") # lop off the prefix
    name = (soup.find('h1', attrs={'itemprop':'name'}).get_text()).strip()
    print name
    yelp_name = restaurant_name
    avg_rating = float(soup.find('meta', {'itemprop':'ratingValue', 'content':True}).attrs['content'])
    location = soup.find('span', attrs={'itemprop':'addressLocality'}).get_text() + ", " + soup.find('span', attrs={'itemprop':'addressRegion'}).get_text()
    stars = 3

    next = soup.find('a', attrs={'class':'next'}) # look for the "next" page link
    
    review_objs_list = []
    for review in soup.findAll('div', class_='review') :
        review_objs_list.append(review)

    review_objs_list = review_objs_list[1:] # first item is dummy
    next_page_reviews = []

    if next:
        next_page_reviews, _ = grab_review_objects(next.attrs['href'], restaurant_name)

    return review_objs_list + next_page_reviews, biz_id


def create_review_dicts(restaurant, existing_dict):
    search_url = search_base_url + restaurant + search_suffix
    review_objs_list, biz_id = grab_review_objects(search_url, restaurant)
    review_dicts_20 = []
    for review in review_objs_list:
        review_dict = {}
        review_dict['review_id'] = review.attrs['data-review-id']
        review_dict['date'] = review.find('meta', attrs={'itemprop':'datePublished', 'content':True}).attrs['content']
        review_dict['rating'] = float(review.find('meta', {'itemprop':'ratingValue', 'content':True}).attrs['content'])
        review_dict['location'] = review.find('li', attrs={'class':'user-location'}).get_text().replace("\n","")
        review_dict['restaurant'] = restaurant
        review_dict['text'] = re.sub(ur'\u00a0','',review.find('p', attrs={'itemprop':'description'}).get_text(),re.UNICODE) # get rid of unicode
        review_dict['biz_id'] = biz_id # primary key in restaurants table, foreign key in reviews table
        review_dicts_20.append(review_dict)

    return existing_dict + review_dicts_20


def load_file(restaurant_name):
    exiting_file = os.path.exists("json/%s.json" % restaurant_name) # make sure you have a json/ folder on the same level as this file
    if exiting_file:
        f = open("json/%s.json" % restaurant_name, "r")
        review_dicts = json.load(f)
        f.close()
    else:
        review_dicts = []
    return review_dicts


def dump_to_file(restaurant_name, review_dicts):
    """ takes 2 args: 
        -name of restaurant - compute name of file
        -list of reviews - all + 20 new ones
        then figures name out name of file, opens it
        and dumps review_dicts into it """

    f = open("json/%s.json" % restaurant_name, "w+")
    json.dump(review_dicts, f, indent=4, separators=(", ", ": "))
    f.close()


def main(restaurant_name, restaurant):
    review_dicts = load_file(restaurant_name)
    review_dicts = create_review_dicts(restaurant, review_dicts)
    dump_to_file(restaurant_name, review_dicts)

if __name__ == "__main__":
    
    search_base_url = "https://www.yelp.com/biz/"
    
    # list of tuples (yelp name, name for file) to scrape multiple restaurants in one run
    # where tuple[0] = restaurant (as listed in yelp url (aka the yelp id)); tuple[1] = short name for output file
    restaurant_list = [("jean-georges-new-york", "jeanGeorges"), ("chefs-table-at-brooklyn-fare-brooklyn-3", "brooklynFare")]

    # restaurant = "benu-san-francisco-4" # change this to the correct retaurant
    # restaurant_name = "benu" # useful for creating/naming the json file or sql table
    search_suffix = "?sort_by=date_desc"
    starting_url = "https://www.yelp.com"

    for item in restaurant_list:
        main(item[1], item[0])
