# Keyword manager for SEO project

## Background
I create this web application to help me finding keyword from Google for doing SEO. it can find Longtail, Refine and Related keyword from Google in real-time. I use web scraping named "Selenium" (Python).

Furthermore, it can manage keyword for doing SEO from defining Title to writing footer content.

## Technology
- Python
- Django Framework
- SQLite3 for Database
- Selenium for web scraping

## Requirement.
- Python 3.0

## How to Deploy on local

### Step 1 : set up Python
1. Download & Install python (https://www.python.org/downloads)
2. Check Python's version by `python -v`

### Step 2 : Set up package in project
1. Open terminal at project folder
2. run command `pip install -r requirements.txt` to install required packages.

### Step 3 : Set up Google Chrome for web scraping
3. Download and Check `Google Chrome` version
4. Download `chromedriver` depend on Google Chrome version for controlling Google Chrome. 
- ex. Google Chrome version 104, You need to download chromedriver version 104.
5. Place downloaded chromedriver to project folder.

### Step 4 : Run project
1. Open terminal at project folder
2. run command `python manage.py runserver` to run project


### Step 5 : Login to web app
1. Open new tab browser
2. Go to `localhost:8000`
3. Login as root
 - username : cheetah
 - password : cheetah

## How to use
- First navigation is finding keyword. You can put any keyword in input box. System will provide keyword from Google for you
- Second navigation is manage keyword. it is a little bit complicated to describe because I designed it for only myself.
- Third navigation is Permission for each user.
- Fourth and Fifth navigation are not complete right now.

