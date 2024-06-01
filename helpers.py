# login_required
from functools import wraps
from flask import session, redirect, url_for

# scrapers
from models import *
import json
import requests
from bs4 import BeautifulSoup
import re

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def which_scraper(websites_list, url):
    "Find which scrape function to use"
    for website in websites_list:
        if website in url:
            return f"scrape_{website}"
            
    return None

def scrape_allerhande(url, time, user_id):
    # Read out dom
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    # Scrape json object
    recipe_json = json.loads(soup.find('div', class_='recipe-details_print__amOMO').next_sibling.text)

    # Save all attributes into recipe
    name = recipe_json['name']
    ingredients = recipe_json['recipeIngredient']

    directions_root = recipe_json['recipeInstructions']
    directions = []
    for step in directions_root:
        directions.append(step['text'])
    
    keywords = recipe_json['keywords']

    if 'zonder vlees' in keywords or 'vegetarisch' in keywords:
        vega = True
    else:
        vega = False

    image = recipe_json['image'][1]
    
    # Return recipe object
    recipe = Recipe(user_id=user_id,name=name,ingredients=ingredients,\
                    directions=directions,keywords=keywords,vega=vega,time=time,image=image,url=url)
    
    print("repobj", recipe.keywords)
    
    return recipe


def scrape_hellofresh(url, time, user_id):
    # Read out dom
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    # Scrap json object
    recipe_json = json.loads(soup.find('script', type='application/ld+json').text)
        
    # Save all attributes into recipe
    name = recipe_json['name']
    ingredients = recipe_json['recipeIngredient']

    directions_root = recipe_json['recipeInstructions'] 
    directions = []
    for step in directions_root:
        sub = re.sub('\n', ' ', step['text']).strip(' ')
        directions.append(sub)

    keywords = ', '.join(recipe_json['keywords'])
    keywords = keywords.lower()

    if 'Veggie' in keywords:
        vega = True
    else: 
        vega = False

    image = recipe_json['image']

    # Return recipe object
    recipe = Recipe(user_id=user_id,name=name,ingredients=ingredients,\
                    directions=directions,keywords=keywords,vega=vega,time=time,image=image,url=url)
    
    return recipe