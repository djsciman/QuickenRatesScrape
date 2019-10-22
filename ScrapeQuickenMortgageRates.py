from bs4 import BeautifulSoup
from requests import get
import requests
import pandas as pd
import itertools

def ScrapeQuickenMortgageRates():
    # Declare our headers
    headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
    # Enter the link to the webpage that we want to scrape
    link = "https://www.quickenloans.com/mortgage-rates"
    # Access the web link we specified above
    response = get(link, headers=headers)

    # Parse the web response and pass it into a BeautifulSoup object
    html_soup = BeautifulSoup(response.text, 'html.parser')
    # Create an empty DataFrame to pass our scrapings into
    dat= pd.DataFrame([])
    # Isolate the boxes on the webpages that contain our data
    RatesBoxes = html_soup.find("div", "o-Wrapper o-Wrapper--wide sls-u-mbm sls-u-pvn").find("section","o-Grid o-Grid--quintuple").find_all("div")
    # Loop through each box and extract the details we're interested in
    for box in RatesBoxes:
        try:
            product = box.find("h2").get_text(strip=True)
            interestrate = box.find("p", "b-Heading--secondary u-TextCenter sls-u-mbn").get_text().replace("%","")
            apr = box.find("p", "b-Heading--secondary u-TextCenter sls-u-mbs").get_text().replace("(","").replace(")","").replace("% APR","")
            row = [[product, interestrate, apr]]
            dat = dat.append(row)
        except AttributeError: # For some reason, at the end of this particular webpage, we get this error. Probably some kind of EOF issue
            pass
    return dat
