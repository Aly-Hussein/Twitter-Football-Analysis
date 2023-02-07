import logging
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


def main():
    # replace user and password in the conncection string
    connectionString = "postgresql://aly:pmhs0rlJl7xFY3BHilr42A@blank-raccoon-8825.7tt.cockroachlabs.cloud:26257/Football?sslmode=verify-full"

    # Connect to CockroachDB
    connection = psycopg.connect(connectionString, application_name="$ football-tables-creation")
    
    statements = [
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
    ]

    for statement in statements:
        exec_statement(connection, statement)

    # Close communication with the database
    connection.close()


if __name__ == "__main__":
    main()