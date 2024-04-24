# web scraping Job finding site

## Background

### What is this for ?
This website was made for helping Thai people who live in Sydney, Australia to find a Thai job easier by removing useless posts and order by latest date.

### Why do this ?
I was studying in Sydney, Australia. In the meantime, I needed to find a job, but in the SydneyThai website, which was a job finding site for Thai people in Australia, is contaminated useless posts around 80%. In addition to the disadvantage, it didn't order by date. Hence, looking for an updated job is almost impossible. I couldn't find a job for myself, so I decided to created this system to scrap all posts, then filter useless posts out. After using for a month, I decided to publish to public at https://aussiethai.net

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
2. Go to `localhost:8000` to see posts
3. Go to `localhost:8000/refresh-check` to refresh jobs to the system.
   
## How to use
- Looking for a job in Home page.

