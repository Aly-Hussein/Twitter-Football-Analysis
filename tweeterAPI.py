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

# Fetches a list of User Objects. 
#The Users that are members of the list id "88096365"
#That list has all the official accounts of the premier league football clubs
def GetListMembers(listId):
    return client.get_list_members(id=listId,user_fields="verified,public_metrics")[0]

# query = '#petday -is:retweet lang:en'
# tweets = tweepy.Paginator(client.search_recent_tweets, query=query,
#                           tweet_fields=['context_annotations', 'created_at'], max_results=100).flatten(limit=1000)

# for tweet in tweets:
#     print(tweet.text)
#     if len(tweet.context_annotations) > 0:
#         print(tweet.context_annotations)
