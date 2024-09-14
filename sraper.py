""" Scraper to fetch data from RedSuburbs """

from bs4 import BeautifulSoup as bs
import requests as req

class Scraper:
    """ Scrapper class to get data """

    def __init__(self) -> None:
        self.url = 'https://redsuburbs.com.au/suburbs/'


    def read_suburb(self) -> list:
        """ function to fetch and normalise the list of suburbs """
        suburbs_csv = open("./suburbs.csv", "r", encoding="utf-8")
        suburb = suburbs_csv.readline()

        suburb_list = []
        while suburb:
            suburb_list.append(suburb.rstrip().lower().replace(" ", "-"))
            suburb = suburbs_csv.readline()
        suburbs_csv.close()

        return suburb_list


    def scraper(self) -> None:
        """ function to scrape data """
        suburbs = self.read_suburb()
        for suburb in suburbs:
            res = req.get(self.url + suburb + "/", timeout=10000)
            print(suburb, res.status_code)
        #soup= bs(res.content, "html.parser")


scrape = Scraper()
scrape.scraper()
