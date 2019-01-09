import json, random
import urllib
from urllib import request

################################################### QUOTES API #################################################

#THIS FUNCTION IS A WORK IN PROGRESS
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
    data = json.loads(info)

    print(data)
    return data

def getQuote():
    
    base_url = "https://quotes.rest/qod?category=inspire"
    url = base_url
    header = {
            "Accept": "application/json",
            }


    r = request.Request(url, headers = header )

    try:
        raw = request.urlopen(r)
    except:
        print("Error0")
        return None


    info = raw.read()
    genres = json.loads(info)

    req = request.Request(url, headers = header)
    raw = request.urlopen(req).read()
    data = json.loads(raw)

    print(data)

    return data

################################################### IPSUM API #################################################
def getIpsum():
    
    base_url = "http://dinoipsum.herokuapp.com/api/?format=json"
    words = "&words=" + str(100) #this 100 can be swapped somehow
    paragraphs = "&paragraphs=" + str(2) #this 2 can be swapped somehow
    url = base_url + words + paragraphs
    header = {
            "Accept": "application/json",
            }


    r = request.Request(url, headers = header )

    try:
        raw = request.urlopen(r).read()
    except:
        print("Error0")
        return None



    data = json.loads(raw)

    print(data)

    return data


################################################### AVATAR API #################################################
def getRandomAvatarLink():
    url = "https://api.adorable.io/avatars/285/" + str(random.randint(0, 10000))
    print(url)
    return url



getQuoteCategories()

