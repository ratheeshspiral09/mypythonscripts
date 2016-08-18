import requests
import sys
import json
from bs4 import BeautifulSoup

keywords = [x.strip() for x in sys.argv[1].split(',')]

no_of_items = 100
result = []


def scraper(url):
    """Scrapper function using beautifulsoup"""

    #hiding ssl warnings
    requests.packages.urllib3.disable_warnings()
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")
    return soup


for keyword in keywords:
    counter = 0
    brands = ["TRESemme", "Himalaya","L'Oreal Paris"]
    page = 0
    response = {}
    response['position'] = {}
    response['keyword'] = keyword
    # check only if anything remaining brand without position or check 100 items completed
    while (counter <= no_of_items and len(brands) > 0):
        page += 1
        key = keyword.replace(' ', '+')
        url = "http://www.amazon.in/s/field-keywords=" + \
            str(key) + "&page=" + str(page)
        soup = scraper(url)
        html_elements = soup.findAll(
            "span", {"class": "a-size-small a-color-secondary"})
        for row in html_elements:
            if row.find(text="by "): #identify span containing "by " text
                counter += 1  # got an item to check
                next_item = row.findNext('span').next #identify the brand name in next span
                for brand in brands:
                    if brand in next_item:
                        # removing brands which we got position from the search list
                        brands.remove(brand)
                        response['position'][brand] = counter
    result.append(response)

final_result={"result":result}
print json.dumps(final_result)
