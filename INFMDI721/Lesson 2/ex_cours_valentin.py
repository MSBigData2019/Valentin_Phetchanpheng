import requests
from bs4 import BeautifulSoup
import pandas as pd

# liste des URLs
list_url = ["https://www.darty.com/nav/achat/informatique/ordinateur_portable/portable/marque__acer__ACER.html",
            "https://www.darty.com/nav/achat/informatique/ordinateur_portable/portable/marque__dell__DELL.html"]

# # On boucle sur la liste des URL
# for url in list_url:
#     page = requests.get(url)
#     soup = BeautifulSoup(page.content, "html.parser")


url = "https://www.darty.com/nav/achat/informatique/ordinateur_portable/portable/marque__acer__ACER.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

# Prix action
prix_solde = []
zone_all_price_ordi = soup.find_all("div", {"class":"prix_barre_liste"})
print(zone_all_price_ordi)
for i in range(0,len(zone_all_price_ordi)):
    prix_solde.append(zone_all_price_ordi[i].find("p", {"class":"darty_prix_barre_remise darty_small separator_top"}))


#print(prix_solde)

    # span_price = zone_price.find_all("span")
    # price = span_price[1]
    # currency = span_price[2]
    # dico_data[span_price[0].text.strip()] = [price.text.strip() + " " + currency.text.strip()]      # On remplit dico avec les data prix
    #
    # # Variation prix en %
    # zone_change = container[1]
    # change = zone_change.find("span", {"class":"valueContentPercent" })
    #
    # module_container = soup.find_all("div", {"class":"moduleBody"})



