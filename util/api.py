import datetime, json, random
import urllib
from urllib import request

################################################### QUOTES API #################################################

#THIS FUNCTION IS A WORK IN PROGRESS
def getQuote():
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    
    file = open('./data/quote.txt')
    quote = file.read()

    if quote == "":
        print("Empty text file!")
        updateQuote()
        
    
    print(today)
    print(quote)
    

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


    quote = json.loads(raw)['contents']['quotes'][0]['quote']

    print(quote)
    return quote

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
def getAvatarLink(username):
    url = "https://api.adorable.io/avatars/285/" + username
    print(url)
    return url





getQuote()
