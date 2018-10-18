import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

url = "https://gist.github.com/paulmillr/2657075"
token_code = '1108f6d9a6607122dcc98db2b926f3a98bacd858'
head = {'Authorization': 'token {}'.format(token_code)}

def get_list_user(url_page):
    page = requests.get(url_page)
    soup = BeautifulSoup(page.content, "html.parser")
    top_user = []
    for i in range(1,257):
        top_user.append(soup.find(text="#"+str(i)).parent.findNext('td').text)
    return top_user

liste_user = get_list_user(url)

def get_login(long_user):
    return long_user[:long_user.find('(')-1]

def get_list_login(list_user):
    list_res = list(map(get_login, list_user))
    return list_res

liste_login = get_list_login(liste_user)

def get_list_mean_stars(list_login):
    url = "https://api.github.com/users/"
    list_mean_stars = []
    dico_user_mean_stars = {}
    dico_user_mean_stars["Login"] = list_login

    for login in list_login:
        get_repo = requests.get(url + str(login) + "/repos", headers=head)
        json_repo = json.loads(get_repo.content)

        sum_stars = 0
        mean_stars = 0

        for repo in json_repo:
            sum_stars += repo['stargazers_count']
        if len(json_repo) == 0:
            mean_stars = 0
        else:
            mean_stars = sum_stars/len(json_repo)
        list_mean_stars.append(round(mean_stars,3))

    dico_user_mean_stars["Mean Stars"] = list_mean_stars
    return dico_user_mean_stars

dico_liste_moyenne = get_list_mean_stars(liste_login)

# Résultat : liste des moyennes des Stars rangées dans l'ordre décroissant dans DataFrame
df_Stars = pd.DataFrame(dico_liste_moyenne)
df_Stars_Sorted = df_Stars.sort_values(by='Mean Stars', ascending=False)
print(df_Stars_Sorted)

