## File Structure: ##

```
yelp_review_viz/
│   README.md
│   runserver.py    
│
└───yelp_review_viz/
    │   __init__.py
    │   views.py
    │   [all .py files]
    │
    ├───static
    │   │
    │   │───css/
    │   │    style files
    │   │
    │   │───js/
    │   │    javascript files
    │   │    
    │   │───img/
    │   │    image files
    │
    └───templates/
    │   *.html files
    │   
```


**To run the server**

From the main project directory:

```sh python
$ python runserver.py
```
All routes should be written to <kdb>views.py</kdb>

All python files should be saved in the same directory as <kdb>__init__.py</kbd>
