from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
import pandas as pd
from selenium import webdriver


def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    mars_news_title, mars_paragraph = mars_news(browser)
    hemis_urls = mars_hemis(browser)

    data = {
        'mars_news_title' : mars_news_title,
        'news_paragraph' : mars_paragraph,
        'featured_image' : featured_image(browser),
        'facts' : mars_facts(),
        'hemispheres' : mars_hemis,
    }
    browser.quit()
    return data

def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)


    html = browser.html
    news_soup = bs(html, 'html.parser')

    try:
        mars_news_title = news_soup.find('div', class_='content_title').text
        mars_paragraph = news_soup.find("div", class_="article_teaser_body").text

    except AttributeError:
        return None, None

    return mars_news_title, mars_paragraph

def featured_image(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    html = browser.html
    image_soup = bs(html, 'html.parser')

    try:
        image_url = image_soup.find('img', class_='headerimage fade-in').get('src')
    except AttributeError:
        return None 

    featured_image_url = f'https://spaceimages-mars.com/{image_url}'
    return  featured_image_url

def mars_facts():
    try:
        mars_df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    mars_df.columns = ['Description','Mars','Earth']
    mars_df.set_index('Description', inplace=True)

    return mars_df.to_html()
    
def mars_hemis(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemis_urls = []
    for hemis in range(4):
        browser.links.find_by_partial_text('Hemisphere')[hemis].click()
        html = browser.html
        hemi_soup = bs(html, 'html.parser')
        title = hemi_soup.find('h2', class_='title').text
        img_url = hemi_soup.find('li').a.get('href')
        hemispheres = {}
        hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'
        hemispheres['title'] = title
        hemis_urls.append(hemispheres)
        browser.back()
    return hemis_urls

if __name__ == "__main__":
    print(scrape_all())