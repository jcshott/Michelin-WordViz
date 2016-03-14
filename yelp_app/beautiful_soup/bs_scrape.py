import json
import os
import re
import urllib2

from bs4 import BeautifulSoup


search_base_url = "https://www.yelp.com/biz/"
restaurant = "benu-san-francisco-4"
restaurant_name = "benu"
search_suffix = "?start=20&sort_by=date_desc"
starting_url = "https://www.yelp.com"



def grab_review_objects(restaurant):
    search_url = search_base_url + restaurant + search_suffix
    contents = urllib2.urlopen(search_url).read()
    soup = BeautifulSoup(contents, "html.parser")
    biz_id = soup.find('a', attrs={'class':'edit-category', 'href':True}).attrs['href'] # grab the yelp biz id
    biz_id = biz_id.replace("/biz_attribute?biz_id=", "") # lop off the prefix
    
    review_objs_list = []
    for review in soup.findAll('div', class_='review') :
        review_objs_list.append(review)

    review_objs_list = review_objs_list[1:] # first item is dummy
    return review_objs_list, biz_id


def create_review_dicts(restaurant, existing_dict):
    review_objs_list, biz_id = grab_review_objects(restaurant)
    review_dicts_20 = []
    for review in review_objs_list:
        review_dict = {}
        review_dict['review_id'] = review.attrs['data-review-id']
        review_dict['date'] = review.find('meta', attrs={'itemprop':'datePublished', 'content':True}).attrs['content']
        review_dict['rating'] = review.find('meta', {'itemprop':'ratingValue', 'content':True}).attrs['content']
        review_dict['location'] = review.find('li', attrs={'class':'user-location'}).get_text().replace("\n","")
        review_dict['restaurant'] = restaurant
        review_dict['text'] = re.sub(ur'\u00a0','',review.find('p', attrs={'itemprop':'description'}).get_text(),re.UNICODE) # get rid of unicode
        review_dicts_20.append(review_dict)
    #print json.dumps(review_dicts_list, indent=4, separators=(", ", ": "))
    return existing_dict + review_dicts_20


def load_file(restaurant_name):
    exiting_file = os.path.exists("json/%s.json" % restaurant_name)
    if exiting_file:
        f = open("json/%s.json" % restaurant_name, "r")
        review_dicts = json.load(f)
        f.close()
    else:
        review_dicts = []
    return review_dicts


def dump_to_file(restaurant_name, review_dicts):
    """ takes 2 args: 
        name of restaurant - compute name of file
        list of reviews - all + 20 new ones
        figure name out name of file, open it
        dump review_dicts into it """

    f = open("json/%s.json" % restaurant_name, "w+")
    json.dump(review_dicts, f, indent=4, separators=(", ", ": "))
    f.close()


def main():
    review_dicts = load_file(restaurant_name)
    review_dicts = create_review_dicts(restaurant, review_dicts)
    dump_to_file(restaurant_name, review_dicts)

if __name__ == "__main__":
    main()