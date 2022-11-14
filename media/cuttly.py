import urllib
import requests


key = "c3e540d4347c9c0738f6c5c04e5004c0747c1"


def shorten_url(url:str, previous_link)-> str:
    if(previous_link):
        return previous_link
    long_url = urllib.parse.quote(url)
    r = requests.get(f'http://cutt.ly/api/api.php?key={key}&short={long_url}')
    data = r.json()['url']
    if data["status"] == 7:
        short_url = data["shortLink"]
        return short_url
    else:
        return url


def delete_link(url:str):
    short_url = urllib.parse.quote(url)
    delete:int = 1
    r = requests.get(f'http://cutt.ly/api/api.php?key={key}&edit={url}&delete')
    data = r
    print(data)
    # if data['status']==1:
    #     print("Success deleting")
    # else:
    #     print("Error deleting")