from pymongo import MongoClient
from pymongo.server_api import ServerApi

# local
conn=MongoClient("mongodb://localhost:27017/test")


# remote
conn = MongoClient("mongodb+srv://shagun:WucMiA4AWKldlleg@cluster0.70i8n.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))

