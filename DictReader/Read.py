import scipy as sci
import math
import numpy as num
import matplotlib as mpl
import matplotlib.pyplot as plot
import codecs as cod
import pandas as pan


#Pomožne funkcije
def isNaN(num):
    return num != num

def array_parser(hash_array):
    return hash_array.strip("[]\"").split("\",\"")

def month_to_num(month):
        date_conversion = {

            "Jan" : 1,
            "Feb" : 2,
            "Mar" : 3,
            "Apr" : 4,
            "May" : 5,
            "Jun" : 6,
            "Jul" : 7,
            "Aug" : 8,
            "Sep" : 9,
            "Oct" : 10,
            "Nov" : 11,
            "Dec" : 12

        }

        return str(date_conversion[month])


#Grafi
def bar_ordered_tuple(list):
    for x,y in list[0:10]:
        plot.bar(x,y)
    plot.show()

def plot_ordered_tuple(list):
    for x,y in list[0:10]:
        plot.plot(x,y)
    plot.show()

def plot_date_df(df, title):
    df.plot('date', 'count')
    plot.title(title)
    plot.xlabel(df["date"])
    plot.ylabel(df["count"])
    plot.show()

def bar_date_df(df, title):
    df.plot.bar('date', 'count')
    plot.title(title)
    plot.xlabel("date")
    plot.ylabel("count")
    plot.xticks(rotation=90)
    plot.show()


#Pretvaranje podatkov
#lot == list of 2value tuples
def dict_to_lot_sort(keys,values):
    out = [(x,y) for x,y in zip(keys,values)]
    out.sort(key=lambda x:x[1], reverse=True)
    return out

def dict_to_df_sort_date(dict):

    out = pan.DataFrame(dict.items(),columns=["date","count"])
    out = out.sort_values(by=['date'],ascending=True)
    print(out)
    return out

def dict_to_lot_nansort(keys,values):
    out = [(x,y) for x,y in zip(keys,values)]
    return out


#Razredi
class DataHoard:
    tweet_filename = "tweets.csv"
    users_filename = "users.csv"

    def __init__(self):

        self.user_dict = {}
        self.hashtags = {}
        self.created = {}
        self.dated_tweets = {}

        self.tweets = pan.read_csv("tweets.csv",delimiter=",",dtype=num.str)
        self.users = pan.read_csv("users.csv",delimiter=",",dtype=num.str)
        self.tweets.fillna("N/A",inplace = True)
        self.users.fillna("N/A",inplace = True)

        self.unique_users = self.tweets.user_key.unique()
        self.num_unique_users = len(self.unique_users)

        self.unique_hashtags = self.tweets.hashtags.unique()
        self.num_unique_hashtags = len(self.unique_hashtags)

        for row in self.users.itertuples(index=False):

            #User dictionary building
            if row[0] not in self.user_dict.keys():
                self.user_dict[row[0]] = User()
            self.user_dict[row[0]].update_user(row)

            #User creation date counting
            if row[10] != "NaN":
                tmp = Date(row[10])
                if tmp.nan:
                    continue
                if tmp.to_string() not in self.created.keys():
                    self.created[tmp.to_string()] = 0
                self.created[tmp.to_string()] += 1

        for row in self.tweets.itertuples(index=False):

            self.user_dict[row[0]].update_tweet(row)

            #Tweet date counting

            if row[3] != "NaN":
                tmp = Date(row[3],tweet=True)
                if tmp.nan:
                    continue
                if tmp.to_string() not in self.dated_tweets.keys():
                    self.dated_tweets[tmp.to_string()] = 0
                self.dated_tweets[tmp.to_string()] += 1

            #if row[3].split()[0] not in self.dated_tweets.keys():
            #    self.dated_tweets[row[3].split()[0]] = 0
            #self.dated_tweets[row[3].split()[0]] += 1

            #Tweet hashtag counting
            for x in array_parser(row[10]):
                if x!="":
                    if x not in self.hashtags.keys():
                        self.hashtags[x] = 0
                    self.hashtags[x] += 1

        self.anal_hash = dict_to_lot_sort(self.hashtags.keys(),self.hashtags.values())
        self.anal_date = dict_to_df_sort_date(self.created)
        self.anal_tweets = dict_to_df_sort_date(self.dated_tweets)

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

        self.tweets = []
        self.hashtags = {}

    def ordered_hashtags(self):
        out =  [(x,y) for x,y in zip(self.hashtags.keys(),self.hashtags.values())]
        out.sort(key=lambda x:x[1], reverse=True)
        return out

    def update_tweet(self,tweet_row):
        self.tweets.append(Tweet(tweet_row))

        for x in array_parser(tweet_row[10]):
            if x != "" or x!= "":
                if x not in self.hashtags.keys():
                    self.hashtags[x] = 0
                self.hashtags[x] += 1

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
        print("Used hashtags: " + str(self.hashtags))


class Tweet:

    def __init__(self,tweet_row):
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


class Date:

    def __init__(self,date_str,tweet=False):
        self.nan = False
        if not tweet:
            array = date_str.split()
            if date_str != "N/A":
                self.month = month_to_num(array[1])
                self.year = array[5]
            else:
                self.nan = True
        else:
            if date_str != "N/A":
                tmp = date_str.split(" ")[0]
                self.month = tmp.split("-")[1]
                self.year =  tmp.split("-")[0]
            else:
                self.nan = True

    def return_val(self):
        return (int(self.year), int(self.month)) if not self.nan else "Not Available"

    def to_string(self):
        return str(self.year + "-" + self.month) if not self.nan else "Not Available"

#Testirna Koda

data = DataHoard()

bar_date_df(data.anal_date, "Account creation by date")
bar_date_df(data.anal_tweets, "Tweet creation by date")

