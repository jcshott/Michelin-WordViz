import json
import os

from models import Restaurants, connect_to_db


def create_pos_dicts(biz_id):
	restaurant = Restaurants.from_biz_id(biz_id)
	pos_dict = restaurant.determine_pos()
	return pos_dict


def dump_to_file(restaurant_name, pos_dict):
    f = open("pos_dicts/%s.json" % restaurant_name, "w+")
    json.dump(pos_dict, f, indent=4, separators=(", ", ": "))
    f.close()

def main(restaurant_name, biz_id):
    pos_dict = create_pos_dicts(biz_id)
    dump_to_file(restaurant_name, pos_dict)

if __name__ == "__main__":

	from runserver import app
	connect_to_db(app)
	print "Connected to DB."

    # list of tuples (name for file, yelp biz id) to analyze parts of speech (pos)
    # yelp biz id is the primary key of the Restaurants table
	restaurant_tups = [("jeanGeorges", "PBUIaPtgnhmdHE3KHglK-g"), ("brooklynFare", "diCW3Pj1PTVRSyol_d7cZw"), ("perSe", "1DfbZ0VsSCg9g1KILmnvzQ"), ("masa", "t7BIiUN0tFg33kySuuQ0aQ"), ("alinea", "pbEiXam9YJL3neCYHGwLUA"), ("benu", "q2EbLD93gEO5uXXx7Pk3bw"), ("elevenMadisonPark", "nRO136GRieGtxz18uD61DA"), ("frenchLaundry", "T20VEwi7AzKbY2TuVEt_ig"), ("grace","34FOiHFyfGECttI8P2al7A"), ("leBernardine","vRrVSB-LegwUwIxpkeRVtQ"), ("manresa","Sq8CeLnv4Psa7c7GEISJgQ"), ("meadowood", "E1tTNluMJj293QifiLLSmA"), ("saison","XGHTrreDK35ciuA8R6naNQ")]

	for tup in restaurant_tups:
		restaurant_name, biz_id = tup[0], tup[1]
		main(restaurant_name, biz_id)