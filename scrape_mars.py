#!/usr/bin/env python
# coding: utf-8

# ******************************************************************************
# # Homework Assignment:
# # 12-Web Scraping and Document Databases - Mission to Mars
# 
# @Author: Jeffery Brown (daddyjab)
# @Date: 2/19/19
# 
# ******************************************************************************
# 

# # Dependencies

# In[1]:


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

# Pretty Print to help with debugging
from pprint import pprint

# Json - IF JSON FILE EXPORT/IMPORT IS NEEDED
# import json

# Time - IF SLEEP OR OTHER TIME FUNCTIONS NEEDED
# import time


# # Scraping

# ## NASA Mars News

# In[2]:


# NASA Mars News website
url_nasa_mars_base = 'https://mars.nasa.gov'
url_nasa_mars_news = url_nasa_mars_base + '/news'
url_nasa_mars_news


# In[3]:


# Setup the Splinter browser
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[4]:


# Use Splinter to navigate to the page
browser.visit( url_nasa_mars_news )

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(browser.html, 'lxml')


# In[5]:


# The articles are in list elements with class 'slide'.
# Get the first of these list elements, which will be the most recent article
news_info = soup.find('li', class_ = 'slide')


# In[6]:


news_info_url = url_nasa_mars_base + news_info.find('a')['href']
news_info_url


# In[7]:


news_info_date = news_info.find('div', class_ = 'list_date').text
news_info_date


# In[8]:


news_info_title = news_info.find('div', class_ = 'content_title').text
news_info_title


# In[9]:


news_info_teaser = news_info.find('div', class_ = 'article_teaser_body').text
news_info_teaser


# In[10]:


news_info_image_url = url_nasa_mars_base + news_info.find('div',class_ = 'list_image').find('img')['src']
news_info_image_url


# In[11]:


# Put all of the Mars News information in a dictionary
news_info_dict = {
    'news_info_date': news_info_date,
    'news_info_title': news_info_title,
    'news_info_teaser': news_info_teaser,
    'news_info_url': news_info_url,
    'news_info_image_url' : news_info_image_url
}
news_info_dict


# In[ ]:





# ## JPL Mars Space Images - Featured Image

# In[12]:


# NASA JPL website
url_nasa_jpl_base = 'https://www.jpl.nasa.gov'
url_nasa_jpl_mars = url_nasa_jpl_base + '/spaceimages/?search=&category=Mars'
url_nasa_jpl_mars


# In[13]:


# Use Splinter to navigate to the page
browser.visit( url_nasa_jpl_mars )

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(browser.html, 'lxml')


# In[14]:


# The articles are in list elements with class 'slide'.
# Get the first of these list elements, which will be the most recent article
featured_image_info = soup.find('a', id = 'full_image')


# In[15]:


featured_image_details_url = url_nasa_jpl_base + featured_image_info['data-link']
featured_image_details_url


# In[16]:


# Click the link to get to the details page,
# so we can get the high resolution featured picture
browser.visit(featured_image_details_url)


# In[17]:


# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(browser.html, 'lxml')


# In[18]:


# Now, get the URL for the high resolution picture
featured_image_details_info = soup.find('img',class_ = 'main_image')

featured_image_url = url_nasa_jpl_base + featured_image_details_info['src']
featured_image_url


# In[19]:


# Also, while we're here... get the image caption, too
featured_image_title = featured_image_details_info['title']
featured_image_title


# In[20]:


# Put all of the JPL Mars Featured Image information in a dictionary
featured_image_dict = {
    'featured_image_title': featured_image_title,
    'featured_image_url': featured_image_url
}
featured_image_dict


# In[ ]:





# ## Mars Weather

# In[21]:


# NASA JPL website
url_twitter_mars_base = 'https://twitter.com/marswxreport?lang=en'
url_twitter_mars = url_twitter_mars_base


# In[22]:


# Use Splinter to navigate to the page
browser.visit( url_twitter_mars )

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(browser.html, 'lxml')


# In[23]:


# The articles are in list elements with class 'slide'.
# Get the first of these list elements, which will be the most recent article
mars_weather_info = soup.find_all('div', class_ = 'tweet')
for mwi in mars_weather_info:
    mwi_item = mwi.find('strong', class_ = 'fullname', string='Mars Weather')
    if mwi_item:
        print( mwi_item )
        break;


# In[24]:


mars_weather = mwi.find('div', class_ = 'js-tweet-text-container').text.strip()
mars_weather


# In[25]:


mars_weather_url = mwi.find('a', class_ = 'twitter-timeline-link')['href']
mars_weather_url


# In[26]:


# Put all of the Twitter Mars Weather information in a dictionary
mars_weather_dict = {
    'mars_weather': mars_weather,
    'mars_weather_url': mars_weather_url
}


# In[ ]:





# ## Mars Facts

# In[27]:


#http://space-facts.com/mars/
url_space_facts_base = 'http://space-facts.com/mars'
url_space_facts = url_space_facts_base


# In[28]:


# Use Splinter to navigate to the page
browser.visit( url_space_facts )


# In[29]:


space_facts_tables_df = pd.read_html(str(browser.html), attrs = {'id':'tablepress-mars'})
mars_facts_df = space_facts_tables_df[0]


# In[30]:


mars_facts_df.rename( columns = {0:'Fact', 1: 'Mars'}, inplace=True )
mars_facts_df


# In[31]:


mars_facts_table = mars_facts_df.to_html( na_rep='', index = False )


# In[ ]:





# ## Mars Hemispheres

# In[32]:


#https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
url_usgs_astro_base = 'https://astrogeology.usgs.gov'
url_usgs_astro = url_usgs_astro_base + '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
url_usgs_astro


# In[33]:


# Use Splinter to navigate to the page
browser.visit( url_usgs_astro )

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(browser.html, 'lxml')


# In[34]:


hemiphere_image_info = soup.find_all('div', class_ = 'description')


# In[35]:


# Initialize a list of hemisphere image information
hemiphere_image_list = []

# Loop through all of the hemispheres listed on the page
for h in hemiphere_image_info:
    
    # Get the image title
    h_title = h.find('h3').text
    
    # Get the URL of the details page (where the full resolution image can be found)
    h_details_url = url_usgs_astro_base + h.find('a', class_ = 'itemLink product-item')['href']
    
    print (h_title)
    print (h_details_url)
    
    # Click to visit the details page
    browser.visit( h_details_url )
    
    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(browser.html, 'lxml')
    
    # Get the link to the full resolution image (1024x1024)
    h_full_image_url = soup.find('div', class_ = 'downloads').find('a')['href']
    print (h_full_image_url)
    
    # Get the description of the full resolution image
    h_full_image_desc = soup.find('div', class_ = 'content').find('p').text
    print( h_full_image_desc )
    print ("-"*40)
    
    # Add a dictionary of this hemisphere info to the list
    h_dict = {
        'h_title': h_title,
        'h_full_image_url': h_full_image_url,
        'h_full_image_desc': h_full_image_desc
    }
    
    hemiphere_image_list.append( h_dict )


# In[ ]:





# ## Consolidate the Gathered Information

# In[36]:


# Populate the gathered information into a single dictionary
mars_info_dict = {
    'news_info_dict': news_info_dict,
    'featured_image_dict': featured_image_dict,
    'mars_weather_dict': mars_weather_dict,
    'mars_facts_table': mars_facts_table,
    'hemiphere_image_list': hemiphere_image_list
}


# In[ ]:





# In[ ]:





# # Store in MongoDB

# In[37]:


# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# In[38]:


# Define database and collection
db = client.mars_info


# In[39]:


db.mars_info.drop()


# In[40]:


result = db.mars_info.insert_one( mars_info_dict )


# In[ ]:





# In[41]:


# Read back what's in the database - just to check
# Display items in MongoDB collection
m_info = db.mars_info.find()


# In[42]:


pprint(m_info[0])


# In[ ]:





# In[ ]:




