import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

# Open Medicaments
# Paracetamol extraire equivalent traitement pour chacun des produits
# Dosage x quantité


# Version sans regex
medicament = 'paracetamol'
url = 'https://www.open-medicaments.fr/api/v1/medicaments?query=' + medicament

def get_list_medicament(url):
    get_liste = requests.get(url)
    json_liste = json.loads(get_liste.content)
    return json_liste

liste = get_list_medicament(url)
print(liste)

df = pd.DataFrame.from_dict(liste)
df = df[['denomination']]
df = df['denomination'].str.split(' ', expand = True)
df.columns = ['Medicament', 'Lab', 'Quantité', 'Unité', 'Type', 'Type Comprimé']
print(df)