"""
Recəppie was made by Sander Heimans
"""

import os
import re

from flask import Flask, session, request, render_template, redirect, url_for, flash
from flask_session import Session
from flask_cors import CORS

from sqlalchemy import func, or_ #,create_engine, 
from werkzeug.security import check_password_hash, generate_password_hash

from models import *
from helpers import *

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from.env file

app = Flask(__name__)

# List compatible websites for which_scraper() to check
SUPPORTED_WEBSITES = ['allerhande', 'hellofresh']


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db.init_app(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)
CORS(app)

@app.route('/')
def index():
    """Display homepage with random recipes"""

    results = db.session.execute(db.select(Recipe).order_by(func.random()).limit(4))

    recipes = [recipe[0] for recipe in results]
    
    return render_template("index.html", recipes=recipes)

@app.route('/extension/add', methods=["POST"])
def extension_add():
    """Let extension add recipe to database"""

    # Import url to be scraped
    url = request.data.decode('utf-8')
    url = eval(url).get('url')

    # Find which scrape function to use, depending on which website was inserted
    scrape_function = which_scraper(SUPPORTED_WEBSITES, url)

    # Don't continue if unscrapable
    if scrape_function == None:
        return "400: This website is not supported by Recəppie"
    
    # Set user_id for extension to 999
    if not session.get('user_id'):
            session['user_id'] = 999

    # Evaluate scrapefunction with corresponding args
    recipe = eval(f"{scrape_function}(\"{url}\", 0, {session['user_id']})")

    db.session.add(recipe)
    db.session.commit()
    
    return "success.html"

@app.route('/add', methods=["GET", "POST"])
@login_required
def add():
    """Add recipe to database"""
    
    # Scrape using helper function depending on source
    if request.method == "POST":
        url = request.form.get("url")
    
        # Find which scrape function to use, depending on which website was inserted
        scrape_function = which_scraper(SUPPORTED_WEBSITES, url)

        if scrape_function == None:
            flash("Ingevoerde website wordt (nog) niet ondersteund!")
            return redirect(url_for('add'))
      
        # Evaluate corresponding scrape function and add recipe to db
        recipe = eval(f"{scrape_function}(\"{url}\", \"{request.form.get('time')}\", {session['user_id']})")

        db.session.add(recipe)
        db.session.commit()
        
        flash("Recept toegevoegd!")
        return redirect(url_for('add'))

    elif request.method == "GET":
        return render_template("add.html")

@app.route('/api/results')
def api_results():
    """Fetch request for application of filters to search results leads here. 
    Applies the filters to the search results. Also recalculates the new filters"""

    # Strip trailing " " and "+" & replace "%20" with " "
    filters = re.sub('%[0-9A-Fa-f][0-9A-Fa-f]', " ", request.full_path.strip(" +")) 
    # Select everything after "filters=" (8 chars): use find() and add 8 chars for "filters="
    filters = filters[filters.find("filters=")+8:].split("+")
    
    query = request.args.get('search').split()
    
    # Search in names or ingredients
    candidates = []
    for word in query:
        candidates.extend(Recipe.query.filter(or_(Recipe.name.ilike("%" + word + "%"), Recipe.ingredients.ilike("%" + word + "%"))).all())
        
        if len(candidates) == 0:
            flash("Geen recepten gevonden")
            return redirect(url_for('search'))
    
    # Apply filters if there are any applied (can check either or all of applied filters)
    if len(filters[0]) != 0:
        # This line checks that the recipe has EITHER of the applied filters
        # candidates = [candidate for candidate in candidates for filter in filters if filter in candidate.keywords.split(', ')]
        
        # In use: This line checks that the recipe has ALL of the applied filters
        candidates = [candidate for candidate in candidates if all(applied_filter in candidate.keywords.split(", ") for applied_filter in filters)]

    # Create dict of filters w/ nr. of occurrences to create html buttons, counting once per occurrence per recipe 
    filters = {}
    for candidate in candidates:
        keywords = set(candidate.keywords.split(', '))
        for filter in keywords:
            if filter not in filters:
                filters[filter.lower()]=1
            else:
                filters[filter]+=1
    
    # Sort by values and convert back to dict
    filters = sorted(filters.items(), key=lambda x: x[1], reverse=True)
    filters = {key: value for (key, value) in filters if value > 1}
    
    return render_template("results.html", results=candidates, filters=filters)

@app.route('/results')
def results():
    """Generate search results by searching each word in the query"""

    # Split query into individual words
    query = request.args.get('search').split()
    
    # Search in names or ingredients
    candidates = []
    for word in query:
        candidates.extend(Recipe.query.filter(or_(Recipe.name.ilike("%" + word + "%"), Recipe.ingredients.ilike("%" + word + "%"))).all())
        
        if len(candidates) == 0:
            flash("Geen recepten gevonden")
            return redirect(url_for('search'))  
        
    # Create dict of filters w/ amounts to create html buttons, counting once per occurrance per recipe 
    filters = {}
    for candidate in candidates:
        keywords = set(candidate.keywords.split(', '))
        for filter in keywords:
            if filter not in filters:
                filters[filter.lower()] = 1
            else:
                filters[filter] += 1
    
    # Sort by values and convert back to dict
    filters = sorted(filters.items(), key=lambda x: x[1], reverse=True)
    filters = {key: value for (key, value) in filters if value > 1}

    print(filters)

    return render_template('search.html', results=candidates, filters=filters, query=" ".join(query))

@app.route('/search', methods=['GET'])
def search():
    """Implement search function"""
    return render_template('search.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    """Register user"""
   
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Error: must provide username")
            return redirect(url_for('register'))
        
        # Ensure password was submitted
        if not request.form.get("password"):
            flash("Error: must provide password")
            return redirect(url_for('register'))
        
        # Ensure password confirmation
        if not request.form.get("password") == request.form.get("confirmation"):
            flash("Error: passwords are not identical")
            return redirect(url_for('register')) 

        # Check that username is unique
        if not User.query.filter_by(username=request.form.get("username")).first() == None:
            flash("Error: username is already taken")
            return redirect(url_for('register')) 

        # Create new user
        user = User(username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    # Present user register form
    else:
        return render_template("register.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session["user_id"] = None

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Error: must provide username")
            return redirect(url_for('login')) 

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Error: must provide password")
            return redirect(url_for('login'))

        # Query database for username
        user = User.query.filter_by(username=request.form.get("username")).first()

        # Check if user exists
        if user == None:
            flash("Error: user doesn't exist")
            return redirect(url_for('login'))
        
        # Check password
        if not check_password_hash(user.hash, request.form.get("password")):
            flash("Error: password invalid")
            return redirect(url_for('login'))

        # Remember which user has logged in
        session["user_id"] = user.id

        # Redirect user to home page
        return redirect(url_for('index'))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect(url_for('index'))

