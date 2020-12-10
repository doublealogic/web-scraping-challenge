#!/usr/bin/env python
# coding: utf-8

# Setup and Dependencies

from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
from splinter import Browser
import time
from webdriver_manager.chrome import ChromeDriverManager

# Sets Up Splinter
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    return browser


def scrape():
    browser = init_browser()

    # NASA Mars News
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    # Finds all News Article Titles on the News Page
    news_soup_titles = news_soup.find_all('div', class_='content_title')

    # Grabs Most recent News Article Title
    recent_title= news_soup_titles[1].get_text()

    # Finds all News Article Paragraph Teasers on the News Page
    news_soup_para= news_soup.find_all('div', class_='article_teaser_body')

    # Grabs Corresponding Article Paragraph Teaser for the most recent news article title
    recent_paragraph= news_soup_para[0].get_text()


    # JPL Mars Space Images - Featured Image
    space_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(space_image_url)
    time.sleep(1)

    image_html = browser.html
    image_soup = BeautifulSoup(image_html, 'html.parser')

    mars_images = image_soup.find_all('article', class_='carousel_item')

    # Grabs url string for featured image
    mars_url = mars_images[0].attrs['style'][23:75]

    # Saves featured image as variable feat_image
    feat_image = 'https://www.jpl.nasa.gov' + mars_url

    # Mars Facts
    facts_url = 'https://space-facts.com/mars/'

    # Grabs table from Mars Facts webpage
    facts_tables = pd.read_html(facts_url)

    facts_table_df = facts_tables[0]
    facts_table_df.columns = ['Parameter of Mars', 'Fact']
    facts_table_df.set_index('Parameter of Mars', inplace=True)

    # Converts the table dataframe into html format
    facts_html = facts_table_df.to_html()


    # Mars Hemispheres
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemi_base = 'https://astrogeology.usgs.gov/'
    browser.visit(hemisphere_url)
    time.sleep(1)

    hemi_html = browser.html
    hemi_soup = BeautifulSoup(hemi_html, 'html.parser')

    hemi_titles = hemi_soup.find_all('div', class_='description')

    hemisphere_image_urls = []

    for hemi_data in hemi_titles:
        hemi_name = hemi_data.find('h3').text
        new_hemi_url = hemi_base + hemi_data.a['href']
        browser.visit(new_hemi_url)
        time.sleep(1)
        
        new_hemi_html = browser.html
        new_hemi_soup = BeautifulSoup(new_hemi_html, 'html.parser')
        
        new_hemi_img = new_hemi_soup.find('div', class_='wide-image-wrapper')
        new_hemi_img_url = new_hemi_img.find('li').a['href']
        
        hemi_dict = {
                        'title': hemi_name,
                        'img_url': new_hemi_img_url
                    }

        # Adds to and Updates Hemisphere Dictionary    
        hemisphere_image_urls.append(hemi_dict)
        browser.back()

    # Creates dictionary from the above scraped data
    mars_dictionary = {
        "news_title": recent_title,
        "news_p": recent_paragraph,
        "featured_image_url": feat_image,
        "fact_table": facts_html,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Closes browser once complete
    browser.quit()

    return mars_dictionary