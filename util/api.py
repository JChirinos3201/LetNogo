import datetime, json, random, sqlite3
import urllib
from urllib import request
from util import db

DB_FILE = "data/tuesday.db"

################################################### QUOTES API #################################################

#CAUTION: DUE TO QUOTE API LIMIT, THIS FUNC HAS NOT BEEN TESTED
def checkQuote():
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    
    #print(today)
    if db.get_quote()['date'] != today:
        try:
            info = updateQuote()
        except:
            info = ["LetNogo is the best language!", 'Joan "HoneyNut" Cheerios', "2019-01-10"]

        db.update_quote(info[0], info[1], info[2])
        
        return False

    return True

def getQuoteCategories():
    category_url = "https://quotes.rest/qod/categories"
    category_header = {
        "Accept": "application/json",
        "X-TheySaidSo-Api-Secret": "student"
    }
    category_request = request.Request(category_url, headers = category_header)

    try:
        raw = request.urlopen(category_request)
    except:
        print(request.urlopen(category_request))
        print("Error0")
        return None

    info = raw.read()
    data = json.loads(info)['contents']['categories']

    categories = []
    for cat in data:
        categories.append(cat)

    print(categories)
    return categories

def updateQuote():
    base_url = "https://quotes.rest/qod?category="

    categories = getQuoteCategories()

    url = base_url + random.choice(categories)

    header = {
            "Accept": "application/json",
            }

    r = request.Request(url, headers = header )

    try:
        raw = request.urlopen(r).read()
    except:
        print("Error: Something went wrong with the request")
        return "Error: Something went wrong with the request"

    info = json.loads(raw)
    quote = info['contents']['quotes'][0]['quote']
    author = info['contents']['quotes'][0]['author']
    date = info['contents']['quotes'][0]['date']

    print(quote, author, date)
    return (quote, author, date)

################################################### IPSUM API #################################################
def getIpsum(numWords, numPara):

    base_url = "http://dinoipsum.herokuapp.com/api/?format=json"
    words = "&words=" + str(numWords)
    paragraphs = "&paragraphs=" + str(numPara)
    url = base_url + words + paragraphs
    header = {
            "Accept": "application/json",
            }


    r = request.Request(url, headers = header )

    try:
        raw = request.urlopen(r).read()
    except:
        print("Error: Something went wrong with the request")
        return "Error: Something went wrong with the request"



    data = json.loads(raw)

    print(data)
    return data


################################################### AVATAR API #################################################
def getAvatarLink(size, username):
    url = "https://api.adorable.io/avatars/{}/{}.png".format(size, username)
    print(url)
    return url

def bodyParts():
    url = "http://avatars.adorable.io/avatars/list"

    #-- Not sure why I can't urlopen "r" w/o internal server error 500
    #r = request.Request(url)
    
    #try:
    #    raw = request.urlopen(r).read()
        
    #except:
    #    print("Error: Something went wrong with the request")
    #    return "Error: Something went wrong with the request"
    
    #info = json.loads(raw)

    info = {"eyes":["eyes1","eyes10","eyes2","eyes3","eyes4","eyes5","eyes6","eyes7","eyes9"],"nose":["nose2","nose3","nose4","nose5","nose6","nose7","nose8","nose9"],"mouth":["mouth1","mouth10","mouth11","mouth3","mouth5","mouth6","mouth7","mouth9"]}
    
    print(info)
    return info
    
def customAvatarLink(eyes, nose, mouth, color): #written by thomas b/c idk if susan wrote
    url = "https://api.adorable.io/avatars/face/{}/{}/{}/{}.png".format(eyes, nose, mouth, color) #color is in hex
    return url
    
