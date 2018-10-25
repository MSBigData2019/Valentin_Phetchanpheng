import requests
from bs4 import BeautifulSoup
import pandas as pd

# liste des URLs
list_url = ["https://www.reuters.com/finance/stocks/financial-highlights/LVMH.PA",
            "https://www.reuters.com/finance/stocks/financial-highlights/AIR.PA",
            "https://www.reuters.com/finance/stocks/financial-highlights/DANO.PA"]

# On boucle sur la liste des URL
for url in list_url:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # On définit le dico pour remplir le DataFrame
    dico_data = {}

    container = soup.find_all("div", {"class":"sectionQuoteDetail"})

    # Prix action
    zone_price = container[0]
    span_price = zone_price.find_all("span")
    price = span_price[1]
    currency = span_price[2]
    dico_data[span_price[0].text.strip()] = [price.text.strip() + " " + currency.text.strip()]      # On remplit dico avec les data prix

    # Variation prix en %
    zone_change = container[1]
    change = zone_change.find("span", {"class":"valueContentPercent" })
    dico_data["Change %"] = [change.text.strip()]   # On remplit dico avec les data variation prix

    module_container = soup.find_all("div", {"class":"moduleBody"})

    # Sales
    sales = module_container[2].find_all("td")
    sales_header = module_container[2].find_all("th", {"class":"data"})

    # Liste contenant les headers Mean, High, Low etc
    list_sales_header = []
    for header in sales_header:
        list_sales_header.append(header.text.replace("\xa0", " "))

    # On remplit dico avec les valeurs
    for i in range(0, len(list_sales_header)):
        dico_data[list_sales_header[i]] = [sales[i+2].text.strip()]

    # Dividends Yield
    dividends = module_container[4].find_all("td")
    dividend_yield_company = dividends[1]
    dividend_yield_industry = dividends[2]
    dividend_yield_sector = dividends[3]
    dico_data["Dividend Company"] = [dividend_yield_company.text]
    dico_data["Dividend Industry"] = [dividend_yield_company.text]
    dico_data["Dividend Sector"] = [dividend_yield_company.text]

    # Part des actionnaires en %
    column_container = soup.find_all("tbody", {"class":"dataSmall"})
    shares_owned = column_container[2].find("td", {"class":"data"})
    dico_data[shares_owned.parent()[0].text.strip()] = [shares_owned.text.strip()]

    # Visualisation des données avec DataFrame
    df = pd.DataFrame(dico_data, index = [soup.title.text])
    print(df)
    print("\n")