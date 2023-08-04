import requests
from bs4 import BeautifulSoup
import re
from lxml import etree
from urllib.request import urlopen


def scrape_google_play_app_data(app_url):
    letter_pattern = r"(?<=\d)[A-Za-z]"
    numbers_pattern = r"\d+(?:\.\d+)?"

    try:
        response = requests.get(app_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            element_average = soup.find('div', class_='TT9eCd')
            average = element_average.text
            pattern = r"\d+\.?\d*"
            average = float(re.search(pattern, average).group())
            element_reviews = soup.find('div', class_='g1rdde')
            reviews = element_reviews.text
            count_reviews = float(re.search(numbers_pattern, reviews).group())
            match = re.search(letter_pattern, reviews)
            if match:
                letter = match.group()
                match letter:
                    case "K":
                        count_reviews *= 1000
                    case "M":
                        count_reviews *= 1000000

            selector = '#yDmH0d > c-wiz.SSPGKf.Czez9d > div > div > div.tU8Y5c > div:nth-child(1) > div > div > c-wiz > div.hnnXjf > ' \
                       'div.JU1wdd > div > div > div:nth-child(2) > div.ClM7O'
            element_downloads = soup.select_one(selector)
            try:
                downloads = element_downloads.text
            except:
                response = urlopen(app_url)
                htmlparser = etree.HTMLParser()
                tree = etree.parse(response, htmlparser)
                xpath = '/html/body/c-wiz[2]/div/div/div[2]/div[1]/div/div/c-wiz/div[2]/div[2]/div/div/div[2]/div[1]'
                element_downloads = tree.xpath(xpath)
                downloads = element_downloads[0].text

            count_downloads = float(re.search(numbers_pattern, downloads).group())
            match = re.search(letter_pattern, downloads)
            if match:
                letter = match.group()
                match letter:
                    case "K":
                        count_downloads *= 1000
                    case "M":
                        count_downloads *= 1000000

            element_latest_update = soup.find('div', class_='xg1aie')
            latest_update = element_latest_update.text

            return average, count_reviews, count_downloads, latest_update
        else:
            print(f"Failed to fetch data from {app_url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error occurred: {e}")
