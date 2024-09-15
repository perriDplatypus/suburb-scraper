""" Scraper to fetch data from RedSuburbs """

from bs4 import BeautifulSoup as bs
import pandas as pd
import requests as req


class Scraper:
    """Scrapper class to get data"""

    def __init__(self) -> None:
        self.url_suburbs_list = "https://redsuburbs.com.au/states/vic/suburbs/page/"
        self.url_suburbs = []
        self.suburb_data = [
            [
                "Suburb",
                "Postcode",
                "Population",
                "Area Size (KM2)",
                "All Crimes",
                "Crimes per 1000 people",
                "Violent Crimes",
                "Property Crimes",
                "Violent Crimes per 1000 people",
                "Property Crimes per 1000 people",
                "suburbs with less Violent Crime (%)",
                "suburbs with less Property Crime (%)",
            ]
        ]

    def read_suburb(self) -> None:
        """function to fetch the list of all urls for the suburbs in Victoria from RedSuburbs"""
        print("Fetching suburb list...")
        for i in range(1, 58):
            res = req.get(self.url_suburbs_list + str(i) + "/", timeout=10000)
            data = bs(res.content, "html5lib")
            for url in data.find_all(
                "a", attrs={"class": "SuburbsPage__suburb-name"}, href=True
            ):
                self.url_suburbs.append(url["href"])
        print("Done!\n\n")

    def scrape_suburb(self) -> None:
        """function to scrape data"""
        print("Fetching data from list of Suburbs...")
        for url_suburb in self.url_suburbs:
            res = req.get(url_suburb, timeout=10000)
            data = bs(res.content, "html5lib")
            heading = data.find(
                "h1", attrs={"class": "Page__title SuburbProfilePage__title"}
            ).text.split(",")
            name = heading[0].replace("Crime rate in ", "")
            postcode = heading[3]
            population = ""
            area = ""
            crimes = ""
            crimes_per = ""
            violent_crimes = ""
            prop_crimes = ""
            violent_crimes_per = ""
            prop_crimes_per = ""
            violent_crimes_less = ""
            property_crimes_less = ""
            for sub in data.find_all("li", attrs={"class": "SuburbProfilePage__stats-item"}):
                property_name = sub.find(
                    "h5",
                    attrs={"class": "SuburbProfilePage__stats-item-title"},
                    recursive=False,
                ).text

                if property_name == "Population":
                    population = sub.find(
                        "p",
                        attrs={"class": "SuburbProfilePage__stats-item-value"},
                        recursive=False,
                    ).text
                elif property_name == "Area size":
                    area = sub.find(
                        "p",
                        attrs={"class": "SuburbProfilePage__stats-item-value"},
                        recursive=False,
                    ).text.replace("km2", "")
                elif property_name == "All Crimes":
                    crimes = sub.find(
                        "p",
                        attrs={"class": "SuburbProfilePage__stats-item-value"},
                        recursive=False,
                    ).text
                elif property_name == "Crimes per 1000 people":
                    crimes_per = sub.find(
                        "p",
                        attrs={"class": "SuburbProfilePage__stats-item-value"},
                        recursive=False,
                    ).text
                elif property_name == "Violent Crimes":
                    violent_crimes = sub.find(
                        "p",
                        attrs={"class": "SuburbProfilePage__stats-item-value"},
                        recursive=False,
                    ).text
                elif property_name == "Property Crimes":
                    prop_crimes = sub.find(
                        "p",
                        attrs={"class": "SuburbProfilePage__stats-item-value"},
                        recursive=False,
                    ).text
                elif property_name == "Violent Crimes per 1000 people":
                    violent_crimes_per = sub.find(
                        "p",
                        attrs={"class": "SuburbProfilePage__stats-item-value"},
                        recursive=False,
                    ).text
                elif property_name == "Property Crimes per 1000 people":
                    prop_crimes_per = sub.find(
                        "p",
                        attrs={"class": "SuburbProfilePage__stats-item-value"},
                        recursive=False,
                    ).text
                elif property_name == "suburbs with less Violent Crimes":
                    violent_crimes_less = sub.find(
                        "p",
                        attrs={"class": "SuburbProfilePage__stats-item-value"},
                        recursive=False,
                    ).text.replace("%", "")
                elif property_name == "suburbs with less Property Crimes":
                    property_crimes_less = sub.find(
                        "p",
                        attrs={"class": "SuburbProfilePage__stats-item-value"},
                        recursive=False,
                    ).text.replace("%", "")

            self.suburb_data.append(
                [
                    name,
                    postcode,
                    population,
                    area,
                    crimes,
                    crimes_per,
                    violent_crimes,
                    prop_crimes,
                    violent_crimes_per,
                    prop_crimes_per,
                    violent_crimes_less,
                    property_crimes_less,
                ]
            )
        print("Done!\n\n")

    def export_data(self):
        """function to exoprt scraped data to csv"""
        print("Exporting to CSV...")
        suburbs = pd.DataFrame(self.suburb_data)
        suburbs.to_csv("./data.csv", index=False)
        print("Done!\n\n\n")

    def run(self) -> None:
        """function to run all the scrapper functions"""
        self.read_suburb()
        self.scrape_suburb()
        self.export_data()


if __name__ == "__main__":
    Scraper().run()
