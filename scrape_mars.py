from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    ### NASA Mars News
    # Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/)
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(5)
    # Collect the latest News Title and Paragraph Text. 
    # Assign the text to variables that you can reference later (news_title and news_p).

    # Latest News Title tag: div class="content_title"
    # Article teaser (need whole para?) tag: div class="article_teaser_body"

    # Retrieve the parent divs for all articles
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('li', class_='slide')[0]
    for result in results:
        news_title = result.find('div', class_='content_title').text
        news_p = result.find('div', class_='article_teaser_body').text

    ### JPL Mars Space Images - Featured Image
    # Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
    url_s = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_s)
    time.sleep(5)
    # Use splinter to navigate the site  
    # find the image url for the current Featured Mars Image  
    # assign the url string to a variable called `featured_image_url`.
    # Make sure to find the image url to the full size `.jpg` image.
    # Make sure to save a complete url string for this image.
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
        
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')

    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')
    relative_image_path = image_soup.find('img', class_="main_image")['src']
    featured_image_url = url_s + relative_image_path

    ### Mars Weather
    # Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en)
    url_t = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_t)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # scrape the latest Mars weather tweet from the page. 
    # Save the tweet text for the weather report as a variable called `mars_weather`.
    mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
 
    ### Mars Facts
    # Visit the Mars Facts webpage [here](http://space-facts.com/mars/)
    url_f = 'http://space-facts.com/mars/'
    # use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # Use Pandas to convert the data to a HTML table string.
    tables = pd.read_html(url_f)
    df = tables[0]
    html_table = df.to_html("table.html")
    
    ### Mars Hemispheres
    # Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) 
    # to obtain high resolution images for each of Mar's hemispheres.

    url_h = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_h)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('div', class_='item')
    titles = []

    for result in results:
        # Retrieve the thread title
        title = result.find('h3').text
        titles.append(title)


    img_urls = []
    counter = 0

    for result in results:
    
        browser.click_link_by_partial_text(titles[counter])
        time.sleep(5)
        
        html = browser.html
        image_soup = BeautifulSoup(html, 'html.parser')
        
        relative_image_path = image_soup.find_all('a')[41]["href"]
        img_url = url_h + relative_image_path
        img_urls.append(img_url)
        
        browser.click_link_by_partial_text('Back')
        time.sleep(5)
        counter = counter + 1

        # Store data in a dictionary
        mars_data = {
            "news_title": news_title,
            "news_p": news_p,
            "featured_image_url": featured_image_url,
            "mars_weather": mars_weather,
            "html_table": html_table,
            "hemisphere_image_urls": {
                "title": title,
                "img_url": img_url
                }
            }
        
        # Close the browser after scraping
        browser.quit()
        
        # Return results
        return mars_data
