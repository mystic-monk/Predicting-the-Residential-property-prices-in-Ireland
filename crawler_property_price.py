# Python3 program for a web crawler for web pages

# Import time module
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup


def webdoc(url):
    """Gets the contents of the web page

    Parameters
    ----------
    url : str
        The url location of the web page
    object : BeautifulSoup
        web page object

    Returns
    -------
    BeautifulSoup object
        a BeautifulSoup object with contents of the web page
    """
    # requests to fetch the HTML content of the website
    source_code = requests.get(url).text

    # BeautifulSoup to parse the HTML content
    return BeautifulSoup(source_code, "lxml")


def main():
    """Generates new urls, fetches the contents and cleans and store the contents

    Parameters
    ----------
    None

    Returns
    -------
    DataFrame
        a dataframe populated with the contents of properties with attributes,
        from all the web pages
    """

    df = pd.DataFrame()

    for page_num in range(1, 17486):

        # record start time
        start = time.time()

        url = (
            "https://ww1.daft.ie/price-register/?d_rd=1&min_price=25000&max_price=5000000&pagenum="
            + str(page_num)
        )
        # get the soup object
        soup = webdoc(url)

        results = soup.find_all("div", {"class": "priceregister-searchresult"})

        for prop_num in range(0, 25):
            # prop_num = 0
            t = results[prop_num]
            Single_Residential = str(t.text).split("\n")
            residential_details = [
                elem.lstrip() for elem in Single_Residential if len(elem.lstrip()) > 0
            ]

            # Some of the addresses do not have the complete address lines hence check
            # each address lengths to ensure the correct population of the fields
            if len(residential_details) == 7:
                Address_Line_2 = residential_details[2].replace(",", "")
                Address_Line_3 = residential_details[3].replace("Co. ", "")
                Selling_Price = residential_details[4].replace("€", "").replace(",", "")
                Date_of_Purchase = residential_details[5].replace("| ", "")
                residential_type = residential_details[6].split("|")

            if len(residential_details) == 6:
                Address_Line_2 = " "
                Address_Line_3 = residential_details[2].replace("Co. ", "")
                Selling_Price = (
                    residential_details[3].replace("€", "").replace(",", ""),
                )
                Date_of_Purchase = residential_details[4].replace("| ", "")
                residential_type = residential_details[5].split("|")

            # House Type
            if len(residential_type) <= 1:
                House_Type = " "
                Bedrooms = "0"
                Bathrooms = "0"

            if len(residential_type) == 2:
                House_Type = residential_type[1].strip()
                Bedrooms = "0"
                Bathrooms = "0"

            if len(residential_type) == 3:
                House_Type = residential_type[1].strip()
                Bedrooms = residential_type[2].replace("Bedrooms ", "").strip()
                Bathrooms = "0"

            if len(residential_type) == 4:
                House_Type = residential_type[1].strip()
                Bedrooms = residential_type[2].replace("Bedrooms ", "").strip()
                Bathrooms = (
                    residential_type[3]
                    .replace("Bathrooms", "")
                    .replace("Bathroom", "")
                    .strip()
                )

            row = {
                "House": residential_details[0],
                "Address_Line_1": residential_details[1],
                "Address_Line_2": Address_Line_2,  # residential_details[2].replace(",", ""),
                "Address_Line_3": Address_Line_3,  # residential_details[3].replace("Co. ", ""),
                "Selling_Price": Selling_Price,  # residential_details[4].replace("€", "").replace(",", ""),
                "Date_of_Purchase": Date_of_Purchase,  # residential_details[5].replace("| ", ""),
                "House_Type": House_Type,
                "Bedrooms": Bedrooms,
                "Bathrooms": Bathrooms,
            }
            df_temp = pd.DataFrame(row, index=[0])

            df = pd.concat([df, df_temp], ignore_index=True)

            # record end time
        end = time.time()
        print(f"Crawled page number : {page_num}, it took {(end-start) * 10**3} ms.")
    return df


if __name__ == "__main__":
    df = main()
    df.to_csv("price_register.csv")
