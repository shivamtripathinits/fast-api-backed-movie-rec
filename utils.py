# from config.db import conn
# from schemas.fns import serializeDict,serializeList
# import json

# def extract_movies_list():
#     return serializeList(conn.moviesdb.movies.find())


# def extract_movies_by_id(m_id):
#     return serializeDict(conn.moviesdb.movies.find_one({'m_id':m_id}))

# def fetch_exact_move(all_movies, ip_movie):
#     for movie in all_movies:
#         if (movie['title'].lower() == ip_movie.lower()):
#             return movie
#     return ''


# def recommend_on_basis_of_name(all_movies, ip_movie, exact_movie_bool, exact_movie):
#     ans = []
#     for movie in all_movies:
#         if (movie['title'].lower() == ip_movie.lower() or movie['title'].lower() in ip_movie.lower() or ip_movie.lower() in movie['title'].lower() 
#         and  (not exact_movie_bool or  movie['m_id'] != exact_movie['m_id'])):
#             ans.append(movie)
#     return ans


# def recommend_on_basis_of_genres(all_movies, ip_movie, exact_movie_bool, exact_movie):
#     ans = []
#     for movie in all_movies:
#         genres_dict = json.loads(movie['genres'])
#         curr_movie_year = movie['release_date'][0:4]
#         ip_genres_dict = json.loads(exact_movie['genres'])
#         ip_year = exact_movie['release_date'][0:4]

#         print (type(genres_dict), type(ip_genres_dict))
#         # break
#         genres = set()
#         ip_genres = set()
#         for gen in genres_dict:
#             genres.add(gen['id'])
#         for gen in ip_genres_dict:
#             ip_genres.add(gen['id'])
#         match = ip_genres.intersection(genres)
#         if len(match) >2 and abs(int(curr_movie_year) - int(ip_year)) < 1:
#             ans.append(movie)
#     return ans


# def fetch_top_2_cast(ip_cast):
#     casts = json.loads(ip_cast['cast'])
#     count = 0
#     original_cast =set()
#     for cast in casts:
#         count += 1
#         original_cast.add(cast['cast_id'])
#         if count > 1:
#             break
#     return original_cast


# def recommend_on_basis_of_cast(all_movies, ip_movie, exact_movie_bool, exact_movie, exact_cast):
#     ans = []
#     original_cast = fetch_top_2_cast(exact_cast)
#     all_movie_credits  = fetch_moves_credits()
#     for credit in all_movie_credits:
#         curr_cast = fetch_top_2_cast(credit)
#         rank = curr_cast.intersection(original_cast)
#         # print (curr_cast, original_cast, rank)
#         if len(rank) > 0:
#             movie = extract_movies_by_id(credit['m_id'])
#             curr_movie_year = movie['release_date'][0:4]
#             ip_year = exact_movie['release_date'][0:4]
#             if abs(int(curr_movie_year) - int(ip_year)) <= 1:
#                 ans.append(extract_movies_by_id(credit['m_id']))
#     return ans


# def fetch_moves_credit_by_id(movie_id):
#     return conn.moviesdb.credits.find_one({ "m_id":movie_id})


# def fetch_moves_credits():
#     return serializeList(conn.moviesdb.credits.find())


# def recommend_combined(list1, list2, list3):
#     ans = []
#     for data in list1:
#         ans.append(data)
#     for data in list2:
#         ans.append(data)
#     for data in list3:
#         ans.append(data)
#     f_ans = []
#     visited = set()
#     for i_ans in ans:
#         m_id = i_ans['m_id']
#         if m_id not in visited:
#             visited.add(m_id)
#             f_ans.append(i_ans)
#     f_ans.sort(key = lambda x:x['popularity'],reverse=True)

#     return f_ans[0:min(10, len(ans))]

# def recommend_movie(ip_movie):
#     all_movies = extract_movies_list()
#     ans = []
#     fans = {}
#     exact_movie = fetch_exact_move(all_movies, ip_movie)
#     exact_movie_bool = False
#     if exact_movie:
#         exact_movie_bool = True
#         exact_cast = fetch_moves_credit_by_id(exact_movie['m_id'])
#     fans['exact match'] = exact_movie
#     fans['recommended_match'] = {}
#     fans['recommended_match']['By Name'] = recommend_on_basis_of_name(all_movies, ip_movie, exact_movie_bool, exact_movie)
#     if exact_movie_bool:
#         fans['recommended_match']['By Genre'] = recommend_on_basis_of_genres(all_movies, ip_movie, exact_movie_bool, exact_movie)
#     if exact_movie_bool:
#         fans['recommended_match']['By Cast'] = recommend_on_basis_of_cast(all_movies, ip_movie, exact_movie_bool, exact_movie, exact_cast)
#     if exact_movie_bool:
#         fans['recommended_match']['final_show_to_user'] = recommend_combined(fans['recommended_match']['By Name'], fans['recommended_match']['By Cast'], fans['recommended_match']['By Genre'])
#     return fans
