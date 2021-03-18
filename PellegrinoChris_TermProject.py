# CS 779 Term Project
# Chris Pellegrino
import pymongo
from pymongo import MongoClient
import json
import csv
import pandas as pd
import os
import dns
import pprint

'''
#programatically convert train_triplets.text to csv file, which I then imported into Mongo Atlas using Mongo Compass
read_file = pd.read_csv (r'/Users/chrispellegrino/Desktop/train_triplets.txt', delimiter = "\t", names = ['user', 'song', 'play_count']) #use pandas to read txt
read_file.to_csv (r'/Users/chrispellegrino/Desktop/train_triplets.csv', index = None) #coverting to csv

csv_file = pd.read_csv (r'/Users/chrispellegrino/Desktop/train_triplets.csv')
print(csv_file.head())
'''


client = pymongo.MongoClient("mongodb+srv://Chris:Cats1992@cluster0.rulwl.mongodb.net/MusicDB?retryWrites=true&w=majority")
db = client.test

#print(client) #shows that connection was made with the MongoDB database
db = client['MusicDB']
song_data = db['MusicCollection']
taste_profile = db['train_triplets']


#1) SIMPLE QUERY

#pprint.pprint(song_data.find_one({"title": "Silent Night"}))



# 2) MORE COMPLEX QUERY THAT PULLS FROM BOTH DATA SETS
'''
result = song_data.aggregate([
  {
    "$match": {
  "artist_name": "Boyz II Men",
  "title": "Silent Night"
    }
  },
  {
    "$lookup": {
      "from": "train_triplets",
      "localField": "song_id",
      "foreignField": "song",
      "as": "song_objects"
    }
  }
])
print(list(result))
'''



'''
# 3)  AGGREGATE FUNCTION: COUNT
print(song_data.count_documents({"artist_name": "Elvis Presley"}))
'''
# Querying from both data sets at once

'''
artist = input("Enter artist name: ") # asks for input from user

result = list(song_data.aggregate([
  {
    "$match": {
      "artist_name": artist #takes input from user and matches it with artist in artist_name field
    }
  },
  {
    "$count": "field_name" # counts the number of songs
  }
]))
print("Songs by " + artist + ": " + str(result[0]["field_name"])) #prints it out
'''


# 4) QUERY THAT PERFORMS AGGREGATE FUNCTION WITHOUT AGGREGATE
'''
# Selects songs from 2003 while only outputting the artist name and song name, while purposely omitting the _id
result = song_data.find({ "year": "2003" }, { "_id": 0, "artist_name": 1, "title": 1 }) # 0 means to exclude the field, 1 means to include it. Everything is 0 by default
items = list(result)

print(json.dumps(items, indent=2))'''

'''
# 5) AGGREGATE FUNCTIONS MATCH and PROJECT
result = song_data.aggregate([
  {
    "$match": { #match works like find function
      "year": "2003" #by matching the year 2003, results are filtered, like WHERE year = "2003"
    }
  },
  {
    "$project": { #works like the second part of find function where fields are included or excluded
      "_id": 0,
      "artist_name": 1,
      "title": 1
    }
  }
])
items = list(result)
print(json.dumps(items, indent=2))'''

[
  {
    "$group": {
      "_id": "$artist_name",
      "songs": {
        "$sum": 1
      }
    }
  },
  {
    "$sort": {
      "songs": -1
     }
  }
]
print(songs)
