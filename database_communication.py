import logging
import tweeterAPI
import os
import psycopg
from psycopg.errors import ProgrammingError

def exec_statement(conn, stmt):
    try:
        with conn.cursor() as cur:
            cur.execute(stmt)
            conn.commit()
    except Exception as e:
        print(e)
        return

def UploadFanToDB(fan,connection):
    exec_statement(connection,"INSERT INTO Football_Fan VALUES ({});".format(fan.id))

def UploadClubToDB(club,connection): 
    exec_statement(connection,"INSERT INTO Football_Fan VALUES ({});".format(club.id))

def UploadTweetToDB(tweet,connection):
	exec_statement(connection,"INSERT INTO Twitter_User VALUES ({},'{}',{},{},{},{},{},{},{});"
		.format(tweet.id,
				tweet.text,
				tweet.created_at,
				tweet.public_metrics["impression_count"],
				tweet.public_metrics["like_count"],
				tweet.public_metrics["reply_count"],
				tweet.public_metrics["retweet_count"],
				tweet.author_id.
				tweet.geo["place_id"]))

def UploadUserToDB(user, isClub,connection):
	exec_statement(connection,"INSERT INTO Twitter_User VALUES ({},'{}','{}',{},{},{},{},{});"
		.format(user.id,
				user.username,
				user.name,
				user.public_metrics["followers_count"],
				user.public_metrics["following_count"],
				user.public_metrics["tweet_count"],
				user.public_metrics["listed_count"],
				user.verified))
	if isClub:
		UploadClubToDB(user,connection)
	else:
		UploadFanToDB(user,connection)

def UploadPlaceToDB(place,connection):
	exec_statement(connection,"INSERT INTO Twitter_Place VALUES ({},'{}','{}','{}');"
		.format(place.id,
				place.name,
				place.country,
				place.type'))

	
def main():
    # replace user and password in the conncection string
    connectionString = "postgresql://aly:pmhs0rlJl7xFY3BHilr42A@blank-raccoon-8825.7tt.cockroachlabs.cloud:26257/Football?sslmode=verify-full"

    # Connect to CockroachDB
    connection = psycopg.connect(connectionString, application_name="$ football-tables-creation")
    
    footballClubs = tweeterAPI.GetListMembers("88096365") 

    for club in footballClubs:
        UploadUserToDB(club,True,connection)

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
	# id varchar(15) PRIMARY KEY,
	# username varchar(15),
	# name varchar(50),
	# followers_count int,
	# following_count int,
	# tweet_count int,
	# listed_count int,
	# verified bool);""",

    # """CREATE Table Football_Fan (
	# id varchar(15) PRIMARY KEY,
	# FOREIGN KEY (id) REFERENCES Twitter_User);""",

    # """CREATE Table Football_Club (
	# id varchar(15) PRIMARY KEY,
	# FOREIGN KEY (id) REFERENCES Twitter_User);""",
    
    # """CREATE TABLE Tweet (
	# id varchar(25) PRIMARY KEY,
	# text text NOT NULL,
	# created_at Date,
	# impression_count int,
	# like_count int,
	# reply_count int,
	# retweet_count int,
	# url_link_clicks int,
	# user_profile_clicks int,
	# author_id varchar(15) REFERENCES Twitter_User ON DELETE CASCADE,
	# location varchar(25) REFERENCES Place);"""
   	