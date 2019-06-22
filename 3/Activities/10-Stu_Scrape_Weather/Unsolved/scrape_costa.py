from splinter import Browser
from bs4 import BeautifulSoup as bs
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    url = "https://visitcostarica.herokuapp.com/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the average temps
    avg_temps = soup.find('div', id='weather')

    other_temps = avg.temps.find_all('strong') 

    '''
    UNCOMMENT LOGIC BELOW TO VIEW TEMPS
    '''

    # for each in other_temps:
    #     print("-"*10)
    #     print(each)

    # print("-"*10)

    # Get the min avg temp
    # @TODO: YOUR CODE HERE!

    # Get the max avg temp
    # @TODO: YOUR CODE HERE!

    # BONUS: Find the src for the sloth image
    # @TODO: YOUR CODE HERE!

    # Store data in a dictionary
    costa_data = {
        "sloth_img": sloth_img,
        "min_temp": min_temp,
        "max_temp": max_temp
    }

    # Quite the browser after scraping
    browser.quit()

    # Return results
    return costa_data