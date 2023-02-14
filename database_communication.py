import logging
import tweeterAPI
import os
import psycopg
from psycopg.errors import ProgrammingError
from datetime import datetime
import string
import time
import argparse

# Parse the command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--nextToken', help='next token to be searched')
args = parser.parse_known_args()

def exec_statement(conn, stmt):
	try:
		with conn.cursor() as cur:
			cur.execute(stmt)
			conn.commit()
	except Exception as e:
		print(e,'/n',stmt)
		return

def UploadFanToDB(fan,connection):
	exec_statement(connection,"INSERT INTO Football_Fan VALUES ({});".format(fan["id"]))

def UploadClubToDB(club,connection): 
	exec_statement(connection,"INSERT INTO Football_Club VALUES ({});".format(club["id"]))

def UploadTweetToDB(tweet,connection):
	exec_statement(connection,"INSERT INTO Tweet VALUES ({},'{}','{}',{},{},{},{},'{}','{}');"
		.format(tweet["id"],
				tweet["text"].replace("'","\""),
				#Parsing the dateTime string from python to a format that the DB can use
				datetime.strptime(tweet["created_at"],"%Y-%m-%dT%H:%M:%S.%fZ").date(),
				tweet["public_metrics"]["impression_count"],
				tweet["public_metrics"]["like_count"],
				tweet["public_metrics"]["reply_count"],
				tweet["public_metrics"]["retweet_count"],
				tweet["author_id"],
				tweet["geo"]["place_id"]))

def UploadUserToDB(user, isClub,connection):
	exec_statement(connection,"INSERT INTO Twitter_User VALUES ({},'{}','{}',{},{},{},{},{});"
		.format(user["id"],
				user["username"],
				user["name"],
				user["public_metrics"]["followers_count"],
				user["public_metrics"]["following_count"],
				user["public_metrics"]["tweet_count"],
				user["public_metrics"]["listed_count"],
				user["verified"]))
	if isClub:
		UploadClubToDB(user,connection)
	else:
		UploadFanToDB(user,connection)

def UploadPlaceToDB(place,connection):
	exec_statement(connection,"INSERT INTO Place VALUES ('{}','{}','{}','{}');"
		.format(place["id"],
				place["full_name"],
				place["country"],
				place["place_type"]))

	
def main():
	# replace user and password in the conncection string
	connectionString = "postgresql://aly:pmhs0rlJl7xFY3BHilr42A@blank-raccoon-8825.7tt.cockroachlabs.cloud:26257/Football?sslmode=verify-full"

	# Connect to CockroachDB
	connection = psycopg.connect(connectionString, application_name="$ football-tables-creation")

	# Prevents Next sql statements from failing if one fails in the middle
	connection._set_autocommit(True)

	if("nextToken" in args):
		response = tweeterAPI.connect_to_endpoint(tweeterAPI.search_url,tweeterAPI.GetQueryParams(args.nextToken))
	else:
		response = tweeterAPI.connect_to_endpoint(tweeterAPI.search_url,tweeterAPI.GetQueryParams())


	tweetList = tweeterAPI.GetTweetsDataList(response)

	for tweet in tweetList:
		if "geo" in tweet:
			userPlace = tweeterAPI.GetUserPlaceTupleFromTweet(tweet)
			UploadUserToDB(userPlace[0],False,connection)
			UploadPlaceToDB(userPlace[1],connection)
			UploadTweetToDB(tweet,connection)

	while(tweeterAPI.GetNextQueryToken(response)):
		print(tweeterAPI.GetNextQueryToken(response))
		try:
			response = tweeterAPI.connect_to_endpoint(tweeterAPI.search_url,tweeterAPI.GetQueryParams(tweeterAPI.GetNextQueryToken(response)))
			tweetList = tweeterAPI.GetTweetsDataList(response)

			for tweet in tweetList:
				if "geo" in tweet:
					userPlace = tweeterAPI.GetUserPlaceTupleFromTweet(tweet)
					UploadUserToDB(userPlace[0],False,connection)
					UploadPlaceToDB(userPlace[1],connection)
					UploadTweetToDB(tweet,connection)
		except Exception as e:
			time.sleep(15 * 60)


	# for user in userList:
	# 	UploadUserToDB(user,False,connection)

	# for place in placeList:
	# 	UploadPlaceToDB(place,connection)

	# tweetList = tweeterAPI.GetTweetsDataList(response)
	# for tweet in tweetList:
	# 	UploadTweetToDB(tweet,connection)

	# Close communication with the database
	connection.close()


if __name__ == "__main__":
	main()

	   