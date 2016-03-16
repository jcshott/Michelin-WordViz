## File Structure: ##


project directory:

/yelp_review_viz

    /runserver.py

    /yelp_review_viz
        /__init__.py
        /views.py
        /static
            /css
            	style files
            /js
            	javascript files
            /img
            	image files
        /templates
            html files

**To run the server**

From the main project directory:

```sh
$ python runserver.py
```
All routes should be written to <kdb>views.py</kdb>

All python files should be saved in the same directory as __init__.py