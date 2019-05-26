import scipy as sci
import math
import numpy as num
import matplotlib as mpl
import matplotlib.pyplot as plot
import codecs as cod
import pandas as pan
import networkx as nx
import re
import  itertools as it
from collections import OrderedDict
import random


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

def powerset(iterable):
    s = list(iterable)
    return set(it.chain.from_iterable(it.combinations(s, r) for r in range(len(s)+1)))

#Grafi

def bar_ordered_tuple(list):
    for x,y in list:
        plot.bar(x,y)
    plot.show()

def plot_ordered_tuple(list):
    for x,y in list[0:10]:
        plot.plot(x,y)
    plot.show()

def plot_date_df(df,title):
    df.plot("date","count")
    plot.title(title)
    plot.xlabel(df["date"])
    plot.ylabel(df["count"])
    plot.show()

def bar_date_df(df,title):
    df.plot.bar("date","count")
    plot.title(title)
    plot.xlabel("date")
    plot.ylabel("count")
    plot.xticks(rotation=90)
    plot.show()




def bar_hash_ratio_tuple(dict):

    index = list(dict.keys())
    index.sort()

    for x in index:

        ind=0
        if dict[x].top_tweets() == []:
            continue
        plot.figure(figsize=(10,10))
        plot.title(x)

        print("Month: "+ x)
        for y,z in dict[x].top_tweets():
            plot.bar(ind,z,color='b',width=0.5)
            ind+=1
        ticks = [x for x,y in dict[x].top_tweets()]
        print("\n Number of unique hashtags: " + str(len(ticks)))
        plot.xticks(range(0,len(dict[x].top_tweets())),ticks,rotation=270)
        plot.ylabel("Times used")
        plot.xlabel("Hashtag")
        print("\n\n")
        plot.show()

def bar_hash_unique_tuple(dict):

    index = list(dict.keys())
    index.sort()

    plot.figure(figsize=(10,10))
    plot.title("Unique tag distribution")

    for x in index:
        print("Month: "+ x)
        ticks = [x for x,y in dict[x].top_tweets()]
        print("Number of unique hashtags: " + str(len(ticks)))
        plot.bar(x,len(ticks),0.5)
        plot.plot(x,dict[x].num/100,color="#000000")
    plot.xticks(range(0,len(index)),index,rotation=90)
    plot.ylabel("Unique hashtags")
    plot.xlabel("Month")
    plot.show()

def quick_dated_tweet(dated_tweets,month_string):

    tweets = dated_tweets[month_string].top_tweets()[1:10]

    for y,z in tweets:
            plot.bar(y,z,color='b',width=0.5)
    ticks = [x for x,y in tweets]
    plot.xticks(range(0,10),ticks,rotation=270)
    plot.title(month_string)
    print("Number of unique hashtags: " + str(len(dated_tweets[month_string].top_tweets())))
    plot.show()
    print("~~~~~~~~~~~~~~~~~~")



#Pretvaranje podatkov
#lot == list of 2value tuples
def dict_to_lot_sort(keys,values):
    out = [(x,y) for x,y in zip(keys,values)]
    out.sort(key=lambda x:x[1], reverse=True)
    return out

def dict_to_df_sort_date(dict):

    out = pan.DataFrame(dict.items(),columns=["date","count"])
    out = out.sort_values(by=['date'],ascending=True)
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
        self.dated_tweet_count = {}

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
                    self.created[tmp.to_string()] = 0                   #CHANGE FROM DAY TO MONTH
                self.created[tmp.to_string()] += 1

        for row in self.tweets.itertuples(index=False):

            self.user_dict[row[0]].update_tweet(row)

            #Tweet date counting

            if row[3] != "NaN":
                tmp = Date(row[3],tweet=True)
                if tmp.nan:
                    continue
                if tmp.to_string() not in self.dated_tweet_count.keys():
                    self.dated_tweet_count[tmp.to_string()] = 0
                    self.dated_tweets[tmp.to_string()] = DateTags(tmp)
                self.dated_tweet_count[tmp.to_string()] += 1
                self.dated_tweets[tmp.to_string()].add_tags(array_parser(row[10]))


            #Tweet hashtag counting
            for x in array_parser(row[10]):
                if x != "":
                    if x not in self.hashtags.keys():
                        self.hashtags[x] = 0
                    self.hashtags[x] += 1

        self.anal_hash = dict_to_lot_sort(self.hashtags.keys(),self.hashtags.values())
        self.anal_date = dict_to_df_sort_date(self.created)
        self.anal_tweets = dict_to_df_sort_date(self.dated_tweet_count)

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
        self.link_stat = {}

        self.tag_set = None
        self.link_set = None

        self.tag_powerset = None
        self.link_powerset = None

    def ordered_hashtags(self):
        out = [(x,y) for x,y in zip(self.hashtags.keys(),self.hashtags.values())]
        out.sort(key=lambda x:x[1], reverse=True)
        return out

    def update_tweet(self,tweet_row):
        self.tweets.append(Tweet(tweet_row))

        for x in array_parser(tweet_row[10]):
            if x != "" or x!= "":
                if x not in self.hashtags.keys():
                    self.hashtags[x] = 0
                self.hashtags[x] += 1

        domain = re.search("(?<=(www\.)).+?(?=([\/]))|(?<=(\/\/)).+?(?=([\/]))",tweet_row[11])

        if domain:
             domain = domain.group(0).strip("www.")
             if domain not in self.link_stat.keys():
                 self.link_stat[domain] = 1
             else:
                 self.link_stat[domain] += 1

        self.tag_set = set(self.hashtags.keys())
        self.link_set = set(self.link_stat.keys())

        #self.tag_powerset = set(powerset(self.tag_set))
        #self.link_powerset = set(powerset(self.link_set))

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
                self.day = array[2]
                self.month = month_to_num(array[1])
                self.year = array[5]
            else:
                self.nan = True
        else:
            if date_str != "N/A":
                tmp = date_str.split(" ")[0]
                self.day = tmp.split("-")[2]
                self.month = tmp.split("-")[1]
                self.year = tmp.split("-")[0]
            else:
                self.nan = True

    def return_val(self):
        return (int(self.year), int(self.month)) if not self.nan else "Not Available"

    def to_string(self):
        return str(self.year + "-" + self.month) if not self.nan else "Not Available"

    def return_val_day(self):
        return (int(self.year), int(self.month), int(self.day)) if not self.nan else "Not Available"

    def to_string_day(self):
        return str(self.year + "-" + self.month + "-" + self.day) if not self.nan else "Not Available"

    def compare_to(self,date):
        return self.to_string == date.to_string()

class DateTags:
    def __init__(self,Date):
        self.date = None
        self.hashtags = {}
        self.num = 0

    def add_tags(self,hash_s,excluded=[]):

        for x in hash_s:
            if x in excluded:
                continue
            if x not in self.hashtags:
                self.hashtags[x] = 1
            else:
                self.hashtags[x] += 1
            self.num += 1

    def top_tweets(self):
        tmp = dict_to_lot_sort(self.hashtags.keys(),self.hashtags.values())
        return tmp


def the_graph(DataHoard,label=True):
    graph = nx.Graph()
    weight_dist = []
    heavy = []
    medium = []
    light = []
    users_of_interest = {}
    for userID in DataHoard.user_dict.keys():
        user = DataHoard.user_dict[userID]
        users_of_interest[user.screen_name] = []
        graph.add_node(user.id)
        if len(user.link_set) == 0 or len(user.tag_set) == 0:
                continue
        for targetID in DataHoard.user_dict.keys():
            if targetID == userID:
                continue

            target = DataHoard.user_dict[targetID]
            graph.add_node(target.id)

            tag_ratio = len(user.tag_set.intersection(target.tag_set))/len(user.tag_set.union(target.tag_set))
            link_ratio = len(user.link_set.intersection(target.link_set))/len(user.link_set.union(target.link_set))


            weight = (tag_ratio+link_ratio)/2


            weight_dist.append(weight)
            if weight==0:
                continue
            elif weight<0.1:
                light.append((user.id,target.id))
                graph.add_edge(user.id,target.id,weight=weight)
                continue
            elif weight<0.5:
                medium.append((user.id,target.id))
                graph.add_edge(user.id,target.id,weight=weight)
                continue
            else:
                heavy.append((user.id,target.id))
                graph.add_edge(user.id,target.id,weight=weight)
                if target.screen_name not in users_of_interest[user.screen_name]:
                    users_of_interest[user.screen_name].append(target.screen_name)
                continue

    pos=nx.spring_layout(graph,k=0.5)

    nx.draw_networkx_nodes(graph,pos,node_size=15,node_color="#000000")
    if label==True:
        nx.draw_networkx_labels(graph,pos)


    nx.draw_networkx_edges(graph,pos,edgelist=light,width=1,alpha=0.1,edge_color='g',style='dotted')
    nx.draw_networkx_edges(graph,pos,edgelist=medium,width=2,alpha=0.3,edge_color='b',style='dashed')
    nx.draw_networkx_edges(graph,pos,edgelist=heavy,width=3,alpha=1,edge_color='r')
    plot.show()

#       Handles of grouped users
#    for x in users_of_interest.keys():
#        if users_of_interest[x]:
#            print(x)
#            for y in users_of_interest[x]:
#                print(y)
#
#            print("~~~~~~~~~~~~~~~~~~~~~~")

#Testirna Koda

#data = DataHoard()

#Account Creation by time
#bar_date_df(data.anal_date, "Account creation by date")

#Tweet Creation by time
#bar_date_df(data.anal_tweets, "Tweet creation by date")

#Most used hashtags
#bar_ordered_tuple(data.anal_hash)

#Inefficient graph slideshow
#bar_hash_ratio_tuple(data.dated_tweets)
#bar_hash_unique_tuple(data.dated_tweets)

#Hashtag analysis on month
#quick_dated_tweet(data.dated_tweets,"2016-09")

#Graph of grouping by links/hashtags
#the_graph(data,label=False)

