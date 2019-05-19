# Mars News

This application provides a Mars News Site, generated through Web Scraping and rendered as a responsive page.

# Technologies Used

* Python, Jupyter Notebook, Flask
* MongoDB, PyMongo
* Web Scraping, BeautifulSoup, Splinter

# Reference

* GitHub: https://github.com/daddyjab/MarsNews
* Web Scraping and Data Exploration (Jupyter Notebook): https://github.com/daddyjab/IWasPoisoned_ETL/blob/master/Extract_IWP_Functions_Illinois_Only.ipynb
* Helper Notebook for Accessing IWP Data in MongoDB: https://github.com/daddyjab/IWasPoisoned_ETL/blob/master/Helper_Accessing_I_Was_Poisoned.ipynb

# Contributions

* Jeffery Brown: Designed and implemented all code for this application.

* Data:
    * NASA Mars News website: https://mars.nasa.gov/news
    * NASA Jet Propulsion Laboratory (JPL) - Space Images: https://www.jpl.nasa.gov/spaceimages
    * Twitter Mars Weather Report: https://twitter.com/marswxreport
    * Space Facts about Mars: http://space-facts.com/mars
    * U.S. Geological Survey - Astrogeology Science Center: https://astrogeology.usgs.gov

# Summary

1. A Jupyter Notebook was created to develop Python code to scrape the multiple Mars data source websites and store the information in a NoSQL database (MongoDB).
2. This code was then consolidated into a single function `scrape()`.  The `scrape()` function was built into a Flask route `/scape`, which scaped the Mars data and updated the MongoDB.
3. The `/` (home) route in the Flask app retrieved the Mars information from the database and passed this as dictionary to the rendered home page `index.html`.
4. The home page used the dictionary to format the text and images into a new format.  The page included a button that would allow the user to perform another scrape of data as needed.

| Figure 1: Sample Mars News Report |
|----------|
| ![Figure 1: Sample Mars News Report is Loading...](docs/MarsNews-sample.png "Figure 1: Sample Mars News Report") |
