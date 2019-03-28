import scipy as sci
import  numpy as num
import matplotlib as plot
import codecs as cod
import pandas as pan


def array_parser(hash_array):
    return hash_array.strip("[]\"").split("\",\"")


class DataHoard:
    tweet_filename = "tweets.csv"
    users_filename = "users.csv"

    def __init__(self):
        self.user_dict = {}

        self.tweets = pan.read_csv("tweets.csv",delimiter=",",dtype=num.str)
        self.dft = pan.DataFrame(self.tweets)
        self.users = pan.read_csv("users.csv",delimiter=",",dtype=num.str)
        self.dfu = pan.DataFrame(self.users)

        self.unique_users = self.tweets.user_key.unique()
        self.num_unique_users = len(self.unique_users)

        self.unique_hashtags = self.tweets.hashtags.unique()
        self.num_unique_hashtags = len(self.unique_hashtags)


        for row in self.users.itertuples(index=False):
            if row[0] not in self.user_dict.keys():
                self.user_dict[row[0]] = User()
            self.user_dict[row[0]].update_user(row)

        for row in self.tweets.itertuples(index=False):
            self.user_dict[row[0]].update_tweet(row)







class User:

    def __init__(self):
        self.id = None
        self.location = None
        self.name = None
        self.follow_count = None
        self.status_count = None
        self.time_zone = None
        self.verified = None
        self.language = None
        self.screen_name = None
        self.description = None
        self.creation_date = None
        self.favourites_count = None
        self.friends_count = None
        self.listed_count = None

        self.tweets = {}

    def update_tweet(self,tweet_row):
        self.tweets[tweet_row[8]] = Tweet()
        self.tweets[tweet_row[8]].update_tweet(tweet_row)

    def update_user(self,user_row):
        self.id = user_row[0]
        self.location = user_row[1]
        self.name = user_row[2]
        self.follow_count = user_row[3]
        self.status_count = user_row[4]
        self.time_zone = user_row[5]
        self.verified = user_row[6]
        self.language = user_row[7]
        self.screen_name = user_row[8]
        self.description = user_row[9]
        self.creation_date = user_row[10]
        self.favourites_count = user_row[11]
        self.friends_count = user_row[12]
        self.listed_count = user_row[13]

    def to_string(self):
        print("User id: " + str(self.id))
        print("Location: " + str(self.location))
        print("Handle: " + str(self.screen_name))
        print("Description: " + str(self.description))


class Tweet:

    def __init__(self):
        self.date = None
        self.date_str = None
        self.rt_count = None
        self.is_rt = None
        self.fav_count = None
        self.text = None
        self.tweet_id = None
        self.source = None
        self.hashtags = None
        self.expanded_url = None
        self.posted = None
        self.mentions = None
        self.rt_status_id = None
        self.replied_to_id = None

    def update_tweet(self,tweet_row):
        self.date = tweet_row[2]
        self.date_str = tweet_row[3]
        self.rt_count = tweet_row[4]
        self.is_rt = tweet_row[5]
        self.fav_count = tweet_row[6]
        self.text = tweet_row[7]
        self.tweet_id = tweet_row[8]
        self.source = tweet_row[9]
        self.hashtags = array_parser(tweet_row[10])
        self.expanded_url = array_parser(tweet_row[11])
        self.posted = tweet_row[12]
        self.mentions = array_parser(tweet_row[13])
        self.rt_status_id = tweet_row[14]
        self.replied_to_id = tweet_row[15]



data = DataHoard()

data.user_dict["247165706"].to_string()


