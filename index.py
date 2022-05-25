from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import ALL_METHODS
from starlette.responses import Response
from schemas.fns import serializeDict,serializeList
from fastapi.templating import Jinja2Templates
# from utils import recommend_movie
from Movies import MovieRecommend
from Users import User
# from config.db import conn 
import json
from fastapi_utils.tasks import repeat_every

from config.db import conn

print(22)
origins = [
    "http://localhost:3000",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
template=Jinja2Templates(directory="htmldirectory")
print(22)
@app.get("/")
async def index(request: Request):    
    kk=serializeList(conn.moviesdb.movies.find())
    response_dict = {}
    response = []
    for i in kk:
        ans = {}
        ans['title'] = i['title']
        # print(type(i), type(i['title']))
        response.append(ans)
    response_dict['data'] = response
    return response_dict


# @app.on_event("startup")
# @repeat_every(seconds=60 * 60)  # 1 hour
# def printit():

@app.get("/recommend_movie")
async def index(request: Request):
    response_dict = {}
    req_movie = request.query_params['movie']  
    movie_recommend = MovieRecommend()
    response_dict['data'] = movie_recommend.recommend_movie(req_movie)
    return response_dict


@app.get("/login")
async def index(request: Request):
    response_dict = {}
    user_id = request.query_params['user_id']  
    add_movies = request.query_params.get('add_movies')
    print (user_id, add_movies)
    user = User(user_id)
    print (user.watched, user.user_id)
    if not user.user_exist:
        return {'logged user' : '', 'watched' :[], 'recommended_movies':[],
        'status':'User does not exist visit http://localhost:8000/create_user/?user_id='+ str(user_id),
        'register here': 'http://localhost:8000/create_user/?user_id=' + str(user_id)}
    status = 'movie not added because either its already watched or it does not exist in our db choose movies from http://localhost:8000/'
    if add_movies and add_movies not in user.watched:
        movie = MovieRecommend()
        all_movies = movie.all_movie_list
        all_movies_names = [x['title'].lower() for x in all_movies]
        if add_movies.lower() in all_movies_names:
            status = 'movie added'
            user.update_user_watched(add_movies)
    recommend_movie = []
    m = MovieRecommend()
    recommend_movie = m.recommend_movie_multiple(user.watched)
    # for movie in user.watched:
    #     m = MovieRecommend()
    #     recommended_movie = m.recommend_movie(movie)
    #     recommend_movie.append(recommended_movie['recommended_match']['final_show_to_user'] )
    return {'logged user' : user.user_id, 'watched' :user.watched, 'status':status, 'recommended_movies':recommend_movie , 'register here' :''}


@app.get("/create_user")
async def index(request: Request):
    response_dict = {}
    user_id = request.query_params['user_id']  
    user = User(user_id)
    user.create_new_user()

    return {'created_user' : user.user_id, 'login_link' : 'http://localhost:8000/login/?user_id=' + str(user_id)}


