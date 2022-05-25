from config.db import conn
from schemas.fns import serializeDict,serializeList
import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi
# mc = MongoClient("mongodb+srv://shagun:WucMiA4AWKldlleg@cluster0.70i8n.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
mc = conn
db=mc['moviesdb']
collection = db['users']
class User():
    def __init__(self, user_id):  
        self.user_id = user_id
        self.user_exist = False
        user_exists = self.check_user_exists()
        if user_exists:
            self.user_exist = True
            print (user_exists)
            self.watched = user_exists['watched']
            print('bef self.watched= ', self.watched)
            cx = [x.lower() for x in self.watched]
            self.watched = self.quicksort(0, len(self.watched)-1, cx)
            print('aft self.watched= ', self.watched)
        else:
            self.watched = []
    def create_new_user(self):
        if not self.user_exist:
            collection.update_one({'user_id':self.user_id },{"$set":{'user_id':self.user_id, 'watched':self.watched}},upsert=True)
    def check_user_exists(self):
        found_user =  conn.moviesdb.users.find_one({'user_id':self.user_id})


        return found_user

    def update_user_watched(self, mname):
        # print(mname)
        # if self.check_user_exists():
        self.watched.append(mname)
        user_dict = {'user_id':self.user_id, 'watched':self.watched}
        # print(user_dict)
        collection.update_one({'user_id':self.user_id },{"$set":user_dict},upsert=True)
        return True
    def partition(self, l, r, watched):
        pivot, ptr = watched[r], l
        for i in range(l, r):
            if watched[i] <= pivot:
                watched[i], watched[ptr] = watched[ptr], watched[i]
                ptr += 1
        watched[ptr], watched[r] = watched[r], watched[ptr]
        return ptr



    def quicksort(self, l, r, watched):
        if len(watched) == 1: # Terminating Condition for recursion. VERY IMPORTANT!
            return watched
        if l < r:
            pi = self.partition(l, r, watched)
            self.quicksort(l, pi-1, watched) # Recursively sorting the left values
            self.quicksort(pi+1, r, watched) # Recursively sorting the right values
        return watched
    

# example = ['ram', 'shyam', 'dog']
# # As you can see, it works for duplicates too
# print(quicksort(0, len(example)-1, example))