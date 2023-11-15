import requests
from pprint import pprint as pp
from deep_translator import GoogleTranslator

# API url : https://spoonacular.com/food-api
# Docs url: https://spoonacular.com/food-api/docs

api_key1='6f37d3059a40482eb0a354a5c5760224'
api_key2='b2a7e7ddacc64c29a22907eb90932ac0'
api_key=api_key1


# type(name)=string, name of the recipe
def id_recipe(name):
    url='https://api.spoonacular.com/recipes/complexSearch?apiKey='+api_key+'&query='+name
    r=requests.request("Get",url)
    return(r.json()['results'][0]['id'])


# gives a healthscore /100, if it doesn't exist, it gives the weight watcher score
def nutriscore_recipe(id_recipe):
    url='https://api.spoonacular.com/recipes/'+str(id_recipe)+'/information?apiKey='+api_key
    r=requests.request("Get",url)
    dico_info=r.json()
    nutriscore=str(dico_info['healthScore'])+' sur 100'
    if int(nutriscore[0:2])==0:
        nutriscore=str(dico_info['weightWatcherSmartPoints'])+' point(s)'
    return(nutriscore)


# type(name)=string, gives a wine which fits to the recipe and a description of the wine
def wine_pairing(name):
    url='https://api.spoonacular.com/food/wine/pairing?apiKey='+api_key+'&food='+name
    r=requests.request("Get",url)
    wine_name=r.json()['pairedWines'][0]
    en_text=r.json()['pairingText']
    fr_text=GoogleTranslator(source='en', target='fr').translate(en_text)
    return(fr_text,wine_name)


# gives a summary of the recipe
def summary_recipe(id_recipe):
    url=' https://api.spoonacular.com/recipes/'+str(id_recipe)+'/summary?apiKey='+api_key
    r=requests.request("Get",url)
    return(r.json()['summary'])

# gives the recipe's website
def site_recipe(id_recipe):
    url='https://api.spoonacular.com/recipes/'+str(id_recipe)+'/information?apiKey='+api_key
    r=requests.request("Get",url)
    return(r.json()['sourceUrl'])

# gives the color associated with the nutriscore
def nutriscore_color(nutriscore):
    if nutriscore!='pas encore défini':
        if int(nutriscore[0:2])>=66:
            return('gr')
        elif int(nutriscore[0:2])<66 and int(nutriscore[0:2])>33:
            return('or')
        else:
            return('em')
    else:
        return('em')
