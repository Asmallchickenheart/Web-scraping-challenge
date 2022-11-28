from splinter import Browser
import pandas as pd
import lxml
from bs4 import BeautifulSoup as bs
import requests
import flask


def scrape():
    # create a dictionary to hold all the scraped data
    mars_data = {
        "data_id": 1
    }
    # create a browser instance
    browser = Browser('chrome', headless=True)

    # visit the Mars News Site
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    print("Visiting: " + url)

    # find the latest news title and paragraph
    news_title = browser.find_by_id('news').find_by_css('.content_title').first.text
    news_p = browser.find_by_id('news').find_by_css('.article_teaser_body').first.text
    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p

    # visit the Mars Space Images Site

    browser.visit('https://spaceimages-mars.com/')

    # find the first image url
    first_image_url = browser.find_by_tag('img')[1]['src']
    mars_data["first_image"] = first_image_url
    print("First Image URL: " + first_image_url)

    # read the table and create a dataframe
    url = "https://galaxyfacts-mars.com/"
    page = requests.get(url)
    soup = bs(page.content, 'html.parser')
    # obtain information from tag <table>
    html_table = soup.find('table', class_='table').prettify()
    mars_data["html_table"] = html_table

    # obtain high-resolution images for each of Mar's hemispheres
    html_doc = requests.get('https://marshemispheres.com/').text
    soup = bs(html_doc, 'html.parser')
    each_web_urls = []
    titles = []

    # find each web url
    for link in soup.select('.item>a'):
        each_web_urls.append("https://marshemispheres.com/" + link['href'])

    # find each title
    for title in soup.select('.description h3'):
        titles.append(title.text)

    # find each img_urls
    img_urls = []
    for each_web_url in each_web_urls:
        browser.visit(each_web_url)
        img_url = browser.find_by_text('Sample')['href']
        img_urls.append(img_url)

    # create a list of dictionaries
    hemisphere_image_urls = []
    for i in range(len(titles)):
        hemisphere_image_urls.append({'title': titles[i], 'img_url': img_urls[i]})

    mars_data["hemisphere_image_urls"] = hemisphere_image_urls

    return mars_data



