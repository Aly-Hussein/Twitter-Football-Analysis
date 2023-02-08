import tweepy

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

#Fetches a tweet using the ID and returns its object
def GetTweet(tweetId):
    return client.get_tweet(id=tweetId,tweet_fields="created_at,public_metrics,author_id,geo",expansions="geo.place_id",place_fields="contained_within,country,country_code,full_name,geo,id,name,place_type")[0]

#Fetches a place using the ID and returns its object
def GetPlace(tweet):
    geo = tweet.geo
    if geo:
        place = geo.place
        if place:
            place_info = {}
            place_info['full_name'] = place.full_name
            place_info['country'] = place.country
            place_info['place_type'] = place.place_type
            place_info['geo_id'] = geo.place_id
            return place_info
    return None

# print(tweet.id)
# print(tweet.text)
# print(tweet.created_at)
# print(tweet.)
# print(tweet.public_metrics["like_count"])
# print(tweet.public_metrics["reply_count"])
# print(tweet.public_metrics["retweet_count"])
# print(tweet.author_id)
# print(tweet.geo["place_id"])

