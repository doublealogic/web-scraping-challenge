# Web Scraping Challenge

## Background

This respository contains a project where I built a web application that scrapes various websites for data related to the Mission to Mars and displays all of this information on an HTML page.

## Part 1 - Scraping

First I needed to use a combination of Jupyter Notebook, BeautifulSoup, Pandas and Requests/Splinter to scrape a few websites.

I made a Jupyter Notebook file called [mission_to_mars.ipynb](mission_to_mars.ipynb) and used it to complete all of my scraping and analysis tasks. 

### NASA Mars News

Here, I scraped the [NASA Mars News Site](https://mars.nasa.gov/news/) and collected the latest News Title and Paragraph Text. With these scraps I assigned the text to the variables `recent_title` and `recent_paragraph` respectively.

## Part 2 - MongoDB and Flask Application