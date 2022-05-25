from csv_to_data import fetch_csv_to_data_dict
from pymongo import MongoClient
from pymongo.server_api import ServerApi
mc=MongoClient()
# mc = MongoClient("mongodb+srv://shagun:WucMiA4AWKldlleg@cluster0.70i8n.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db=mc['moviesdb']

print(db)
def csv_to_mongo():
    collection_pdfs=db['movies']
    url = r'..\Backend\tmdb_5000_movies.csv'
    data, data_dict = fetch_csv_to_data_dict(url)
    print (len(data_dict))
    for item in data_dict:
        print(item.keys())
        collection_pdfs.update_one({'m_id':item['id']},{"$set":item},upsert=True)
    collection_pdfs=db['credits']
    url =r'Backend\tmdb_5000_credits.csv'
    data, data_dict = fetch_csv_to_data_dict(url)
    print (len(data_dict))
    for item in data_dict:
        print(item.keys())
        collection_pdfs.update_one({'m_id':item['movie_id']},{"$set":item},upsert=True)

csv_to_mongo()