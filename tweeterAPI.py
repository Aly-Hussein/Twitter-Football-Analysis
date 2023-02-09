import json
import tweepy
import requests

consumer_key = 'cfrMAw09ZamTi6NKP7ezSTXaV'
consumer_secret = '1ZwTmmpzoY6T4rGStowDPEbJ19DZE3rMQoyIQuwD9IGfGi0Oas'
access_token = '2678888678-ESNlkqb0vGreILGiGf0PY8HPPBt1gK2ZxzQosbf'
access_token_secret = 'osuSgYh8zlK1fSH61Y9bCd1QycZK22wgrdlGODJmVA5QK'
bearer_token = "AAAAAAAAAAAAAAAAAAAAAFErlgEAAAAAQlwzw687lovy6gA3OZ0TAoJCIvM%3DnB8LtAhyBR4xNq1C9KBik9ahFJYb0tn4RybG9OWNl5Gtuwbvl8"

client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret,
                       access_token=access_token, access_token_secret=access_token_secret,
                       bearer_token=bearer_token
                       )

#Fetches a list using the listId. 
#Returns all the User members of that list 
#The list with ID "88096365" has all the official accounts of the premier league football clubs
def GetListMembers(listId):
    return client.get_list_members(id=listId,user_fields="verified,public_metrics")[0]

#Function for authentication, don't really understand what it means but its important
def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r

def GetTweetsUrl(ids):
    return ("https://api.twitter.com/2/tweets?ids={}&expansions=geo.place_id,author_id"
            "&place.fields=country,full_name,id,place_type&user.fields=verified,public_metrics"
            "&tweet.fields=created_at,public_metrics,author_id,geo".format(ids))

def GetTweetsResponse(ids):
    return requests.request("GET", GetTweetsUrl(ids), auth=bearer_oauth)

def GetTweetsDataList(response):
    return response.json()["data"]

def GetPlacesDataList(response):
    return response.json()["includes"]["places"]

def GetUsersDataList(response):
    return response.json()["includes"]["users"]