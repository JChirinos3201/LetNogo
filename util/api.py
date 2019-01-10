import datetime, json, random
import urllib
from urllib import request
from util import database

DB_FILE = "data/tuesday.db"

################################################### QUOTES API #################################################

#CAUTION: DUE TO QUOTE API LIMIT, THIS FUNC HAS NOT BEEN TESTED
def checkQuote():
    today = datetime.datetime.today().strftime('%Y-%m-%d')

    data = database.DB_Manager(DB_FILE)

    data.creates_quotes()
    print(today)
    if data.get_quote()['date'] != today:

        try:
            info = updateQuote()
        except:
            info = ["LetNogo is the best language!", 'Joan "HoneyNut" Cheerios', "2019-01-10"]

        data.update_quote(info[0], info[1], info[2])
        data.save()
        return False

    data.save()
    return True

    #-------- IGNORE -------
    #with open('./data/quote.txt') as textfile:
    #    quote = textfile.read()

    #if quote == "":
    #    print("Empty text file!")
    #    updateQuote()
    #-----------------------


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
