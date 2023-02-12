import logging
import tweeterAPI
import os
import psycopg
from psycopg.errors import ProgrammingError
from datetime import datetime
import string

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

	response = tweeterAPI.connect_to_endpoint(tweeterAPI.search_url,tweeterAPI.GetQueryParams())
	# response = tweeterAPI.connect_to_endpoint(tweeterAPI.GetTweetsUrl("1624639389933481985"))

	tweetList = tweeterAPI.GetTweetsDataList(response)

	for tweet in tweetList:
		if "geo" in tweet:
			userPlace = tweeterAPI.GetUserPlaceTupleFromTweet(tweet)
			UploadUserToDB(userPlace[0],False,connection)
			UploadPlaceToDB(userPlace[1],connection)
			UploadTweetToDB(tweet,connection)

	while(tweeterAPI.GetNextQueryToken(response)):
		response = tweeterAPI.connect_to_endpoint(tweeterAPI.search_url,tweeterAPI.GetQueryParams(tweeterAPI.GetNextQueryToken(response)))

		tweetList = tweeterAPI.GetTweetsDataList(response)

		for tweet in tweetList:
			if "geo" in tweet:
				userPlace = tweeterAPI.GetUserPlaceTupleFromTweet(tweet)
				UploadUserToDB(userPlace[0],False,connection)
				UploadPlaceToDB(userPlace[1],connection)
				UploadTweetToDB(tweet,connection)


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

# DDL SQL I ran to create the database
	#    """CREATE TABLE Place (
	#id varchar(25) PRIMARY KEY,
	#full_name text,
	#country varchar(60),
	#place_type varchar(60))"""
	
	# """CREATE TABLE Twitter_User (
	# id varchar(25) PRIMARY KEY,
	# username varchar(15),
	# name varchar(50),
	# followers_count int,
	# following_count int,
	# tweet_count int,
	# listed_count int,
	# verified bool);""",

	# """CREATE Table Football_Fan (
	# id varchar(25) PRIMARY KEY,
	# FOREIGN KEY (id) REFERENCES Twitter_User);""",

	# """CREATE Table Football_Club (
	# id varchar(25) PRIMARY KEY,
	# FOREIGN KEY (id) REFERENCES Twitter_User);""",
	
	# """CREATE TABLE Tweet (
	# id varchar(25) PRIMARY KEY,
	# text text NOT NULL,
	# created_at Date,
	# impression_count int,
	# like_count int,
	# reply_count int,
	# retweet_count int,
	# author_id varchar(25) REFERENCES Twitter_User ON DELETE CASCADE,
	# location varchar(25) REFERENCES Place);"""
	   