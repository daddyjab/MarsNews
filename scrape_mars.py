# ******************************************************************************
# # Homework Assignment:
# # 12-Web Scraping and Document Databases - Mission to Mars
# 
# @Author: Jeffery Brown (daddyjab)
# @Date: 2/19/19
# 
# ******************************************************************************
# 

# # Dependencies  ********************************************

# Pandas for DataFrames
import pandas as pd

# Web Requests
import requests

# Splinter and BeautifulSoup for Web Scraping (+ Pandas)
from splinter import Browser
from bs4 import BeautifulSoup

# SQLAlchemy and PyMongo for MongoDB operations
from sqlalchemy import create_engine
import pymongo

# Time for Last Update info
import datetime as dt

# Pretty Print to help with debugging
from pprint import pprint

def scrape():

    # # Scraping ********************************************

    # ## NASA Mars News

    # NASA Mars News website
    url_nasa_mars_base = 'https://mars.nasa.gov'
    url_nasa_mars_news = url_nasa_mars_base + '/news'
    url_nasa_mars_news

    # Setup the Splinter browser
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    # Use Splinter to navigate to the page
    browser.visit( url_nasa_mars_news )

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(browser.html, 'lxml')

    # The articles are in list elements with class 'slide'.
    # Get the first of these list elements, which will be the most recent article
    news_info = soup.find('li', class_ = 'slide')

    news_info_url = url_nasa_mars_base + news_info.find('a')['href']
    news_info_url

    news_info_date = news_info.find('div', class_ = 'list_date').text
    news_info_date

    news_info_title = news_info.find('div', class_ = 'content_title').text
    news_info_title

    news_info_teaser = news_info.find('div', class_ = 'article_teaser_body').text
    news_info_teaser

    news_info_image_url = url_nasa_mars_base + news_info.find('div',class_ = 'list_image').find('img')['src']
    news_info_image_url

    # Put all of the Mars News information in a dictionary
    news_info_dict = {
        'news_info_date': news_info_date,
        'news_info_title': news_info_title,
        'news_info_teaser': news_info_teaser,
        'news_info_url': news_info_url,
        'news_info_image_url' : news_info_image_url
    }
    news_info_dict

    # ## JPL Mars Space Images - Featured Image  ********************************************

    # NASA JPL website
    url_nasa_jpl_base = 'https://www.jpl.nasa.gov'
    url_nasa_jpl_mars = url_nasa_jpl_base + '/spaceimages/?search=&category=Mars'
    url_nasa_jpl_mars

    # Use Splinter to navigate to the page
    browser.visit( url_nasa_jpl_mars )

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(browser.html, 'lxml')

    # The articles are in list elements with class 'slide'.
    # Get the first of these list elements, which will be the most recent article
    featured_image_info = soup.find('a', id = 'full_image')

    featured_image_details_url = url_nasa_jpl_base + featured_image_info['data-link']
    featured_image_details_url

    # Click the link to get to the details page,
    # so we can get the high resolution featured picture
    browser.visit(featured_image_details_url)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(browser.html, 'lxml')

    # Now, get the URL for the high resolution picture
    featured_image_details_info = soup.find('img',class_ = 'main_image')

    featured_image_url = url_nasa_jpl_base + featured_image_details_info['src']
    featured_image_url

    # Also, while we're here... get the image caption, too
    featured_image_title = featured_image_details_info['title']
    featured_image_title

    # Put all of the JPL Mars Featured Image information in a dictionary
    featured_image_dict = {
        'featured_image_title': featured_image_title,
        'featured_image_url': featured_image_url
    }
    featured_image_dict

    # ## Mars Weather  ********************************************

    # NASA JPL website
    url_twitter_mars_base = 'https://twitter.com/marswxreport?lang=en'
    url_twitter_mars = url_twitter_mars_base

    # Use Splinter to navigate to the page
    browser.visit( url_twitter_mars )

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(browser.html, 'lxml')

    # The articles are in list elements with class 'slide'.
    # Get the first of these list elements, which will be the most recent article
    mars_weather_info = soup.find_all('div', class_ = 'tweet')
    for mwi in mars_weather_info:
        mwi_item = mwi.find('strong', class_ = 'fullname', string='Mars Weather')
        if mwi_item:
            # print( mwi_item )
            break

    mars_weather = mwi.find('div', class_ = 'js-tweet-text-container').text.strip()
    mars_weather

    mars_weather_url = mwi.find('a', class_ = 'twitter-timeline-link')['href']
    mars_weather_url

    # Put all of the Twitter Mars Weather information in a dictionary
    mars_weather_dict = {
        'mars_weather': mars_weather,
        'mars_weather_url': mars_weather_url
    }


    # ## Mars Facts  ********************************************

    #http://space-facts.com/mars/
    url_space_facts_base = 'http://space-facts.com/mars'
    url_space_facts = url_space_facts_base

    # Use Splinter to navigate to the page
    browser.visit( url_space_facts )

    space_facts_tables_df = pd.read_html(str(browser.html), attrs = {'id':'tablepress-mars'})
    mars_facts_df = space_facts_tables_df[0]

    mars_facts_df.rename( columns = {0:'Fact', 1: 'Mars'}, inplace=True )
    mars_facts_df

    mars_facts_table = mars_facts_df.to_html( na_rep='', index = False )

    # ## Mars Hemispheres  ********************************************

    #https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
    url_usgs_astro_base = 'https://astrogeology.usgs.gov'
    url_usgs_astro = url_usgs_astro_base + '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    url_usgs_astro

    # Use Splinter to navigate to the page
    browser.visit( url_usgs_astro )

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(browser.html, 'lxml')

    hemiphere_image_info = soup.find_all('div', class_ = 'description')

    # Initialize a list of hemisphere image information
    hemiphere_image_list = []

    # Loop through all of the hemispheres listed on the page
    for h in hemiphere_image_info:
        
        # Get the image title
        h_title = h.find('h3').text
        
        # Get the URL of the details page (where the full resolution image can be found)
        h_details_url = url_usgs_astro_base + h.find('a', class_ = 'itemLink product-item')['href']
        
        # print (h_title)
        # print (h_details_url)
        
        # Click to visit the details page
        browser.visit( h_details_url )
        
        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(browser.html, 'lxml')
        
        # Get the link to the full resolution image (1024x1024)
        h_full_image_url = soup.find('div', class_ = 'downloads').find('a')['href']
        # print (h_full_image_url)
        
        # Get the description of the full resolution image
        h_full_image_desc = soup.find('div', class_ = 'content').find('p').text
        # print( h_full_image_desc )
        # print ("-"*40)
        
        # Add a dictionary of this hemisphere info to the list
        h_dict = {
            'h_title': h_title,
            'h_full_image_url': h_full_image_url,
            'h_full_image_desc': h_full_image_desc
        }
        
        hemiphere_image_list.append( h_dict )

    # Obtain the current time as a timestamp for this scrape
    update_timestamp = dt.datetime.now().strftime('%c')

    # ## Consolidate the Gathered Information  ********************************************

    # Populate the gathered information into a single dictionary
    mars_info_dict = {
        'update_timestamp': update_timestamp,
        'news_info_dict': news_info_dict,
        'featured_image_dict': featured_image_dict,
        'mars_weather_dict': mars_weather_dict,
        'mars_facts_table': mars_facts_table,
        'hemiphere_image_list': hemiphere_image_list
    }


    # Return the results
    return mars_info_dict
