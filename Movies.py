from config.db import conn
from csv_to_data import fetch_csv_to_data_dict_v2
from schemas.fns import serializeDict,serializeList
import json
class MovieRecommend():
    def __init__(self) -> None:
        self.all_movie_list = self.extract_movies_list()
        self.all_credits_list = self.fetch_moves_credits()

    # slow in remote version
    # def extract_movies_list(self):
    #     return serializeList(conn.moviesdb.movies.find())
    
    # for remote version use this one
    def extract_movies_list(self):
        url = r'..\Backend\tmdb_5000_movies.csv'
        data, data_dict = fetch_csv_to_data_dict_v2(url)
        return serializeList(data_dict)

    # def extract_movies_by_id(self, m_id):
    #     return serializeDict(conn.moviesdb.movies.find_one({'m_id':m_id}))


    def extract_movies_by_id(self, m_id):
        for movie in self.all_movie_list:
            if movie['m_id'] == m_id:
                return serializeDict(movie)
        return serializeDict(movie)


    def fetch_exact_move(self, all_movies, ip_movie):
        for movie in all_movies:
            if (movie['title'].lower() == ip_movie.lower()):
                return movie
        return ''

    def fetch_exact_move_multiple(self, all_movies, ip_movie_list):
        ans = []
        for ip_movie in ip_movie_list:
            for movie in all_movies:
                if (movie['title'].lower() == ip_movie.lower()):
                    ans.append(movie)
        return ans

    def recommend_on_basis_of_name(self, all_movies, ip_movie, exact_movie_bool, exact_movie):
        ans = []
        for movie in all_movies:
            if (movie['title'].lower() == ip_movie.lower() or  ip_movie.lower() in movie['title'].lower() 
            and  (not exact_movie_bool or  movie['m_id'] != exact_movie['m_id'])):
                ans.append(movie)
        return ans
    
    def recommend_on_basis_of_name_multiple(self, all_movies, ip_movie_list, exact_movie_bool, exact_movie_list):
        ans = []
        for ip_movie in ip_movie_list:
            for movie in all_movies:
                if (movie['title'].lower() == ip_movie.lower() or  ip_movie.lower() in movie['title'].lower() ):
                    ans.append(movie)
        return ans


    def recommend_on_basis_of_genres(self, all_movies, ip_movie, exact_movie_bool, exact_movie):
        ans = []
        for movie in all_movies:
            genres_dict = json.loads(movie['genres'])
            curr_movie_year = movie['release_date'][0:4]
            ip_genres_dict = json.loads(exact_movie['genres'])
            ip_year = exact_movie['release_date'][0:4]

            # print (type(genres_dict), type(ip_genres_dict))
            # break
            genres = set()
            ip_genres = set()
            for gen in genres_dict:
                genres.add(gen['id'])
            for gen in ip_genres_dict:
                ip_genres.add(gen['id'])
            match = ip_genres.intersection(genres)
            if len(match) >2 and abs(int(curr_movie_year) - int(ip_year)) < 1:
                ans.append(movie)
        return ans

    def recommend_on_basis_of_genres_multiple(self, all_movies, ip_movie_list, exact_movie_bool, exact_movie_list):
        ans = []
        for exact_movie in exact_movie_list:
            for movie in all_movies:
                genres_dict = json.loads(movie['genres'])
                curr_movie_year = movie['release_date'][0:4]
                ip_genres_dict = json.loads(exact_movie['genres'])
                ip_year = exact_movie['release_date'][0:4]

                # print (type(genres_dict), type(ip_genres_dict))
                # break
                genres = set()
                ip_genres = set()
                for gen in genres_dict:
                    genres.add(gen['id'])
                for gen in ip_genres_dict:
                    ip_genres.add(gen['id'])
                match = ip_genres.intersection(genres)
                if len(match) >2 and abs(int(curr_movie_year) - int(ip_year)) < 1:
                    ans.append(movie)
        return ans

    def fetch_top_2_cast(self, ip_cast):
        casts = json.loads(ip_cast['cast'])
        count = 0
        original_cast =set()
        for cast in casts:
            count += 1
            original_cast.add(cast['cast_id'])
            if count > 1:
                break
        return original_cast


    def recommend_on_basis_of_cast(self, all_movies, ip_movie, exact_movie_bool, exact_movie, exact_cast):
        ans = []
        original_cast = self.fetch_top_2_cast(exact_cast)
        all_movie_credits  = self.all_credits_list
        for credit in all_movie_credits:
            curr_cast = self.fetch_top_2_cast(credit)
            rank = curr_cast.intersection(original_cast)
            # print (curr_cast, original_cast, rank)
            if len(rank) > 0:
                movie = self.extract_movies_by_id(credit['m_id'])
                curr_movie_year = movie['release_date'][0:4]
                ip_year = exact_movie['release_date'][0:4]
                if abs(int(curr_movie_year) - int(ip_year)) <= 1:
                    ans.append(movie)
        return ans
    def recommend_on_basis_of_cast_multiple(self, all_movies, ip_movie_list, exact_movie_bool, exact_movie_list, exact_cast_list):
        ans = []
        all_movie_credits  = self.all_credits_list
        all_movies = self.all_movie_list
        all_movies_dict = {x['m_id']:x for x in all_movies}
        for credit in all_movie_credits:
            curr_cast = self.fetch_top_2_cast(credit)
            movie = all_movies_dict.get(credit['m_id'])
            for exact_cast, exact_movie in zip(exact_cast_list, exact_movie_list):
                original_cast = self.fetch_top_2_cast(exact_cast)
                rank = curr_cast.intersection(original_cast)
                # print (curr_cast, original_cast, rank)
                if len(rank) > 0:
                    curr_movie_year = movie['release_date'][0:4]
                    # exact_movie = self.extract_movies_by_id(exact_cast['m_id'])
                    ip_year = exact_movie['release_date'][0:4]
                    if abs(int(curr_movie_year) - int(ip_year)) <= 1:
                        ans.append(movie)
        return ans


    # def fetch_moves_credit_by_id(self, movie_id):
    #     return conn.moviesdb.credits.find_one({ "m_id":movie_id})

    def fetch_moves_credit_by_id(self, movie_id):
        for credit in self.all_credits_list:
            if credit['m_id'] == movie_id:
                return serializeDict(credit)

        return serializeDict(credit)


    def fetch_moves_credit_by_id_multiple(self, movies_list):
        mid_to_credit_dict = {c['m_id']:c for c in self.all_credits_list}
        ans = []
        for movie in  movies_list:
            if mid_to_credit_dict.get(movie['m_id']):
                ans.append(mid_to_credit_dict.get(movie['m_id']))
        return ans

    # def fetch_moves_credits(self):
    #     return serializeList(conn.moviesdb.credits.find())
    def fetch_moves_credits(self):
        url =r'..\Backend\tmdb_5000_credits.csv'
        data, data_dict = fetch_csv_to_data_dict_v2(url)
        return serializeList(data_dict)
    def recommend_combined(self, list1, list2, list3):
        ans = []
        for data in list1:
            ans.append(data)
        for data in list2:
            ans.append(data)
        for data in list3:
            ans.append(data)
        f_ans = []
        visited = set()
        for i_ans in ans:
            m_id = i_ans['m_id']
            if m_id not in visited:
                visited.add(m_id)
                f_ans.append(i_ans)
        f_ans.sort(key = lambda x:x['popularity'],reverse=True)

        return f_ans[0:min(10, len(ans))]

    def recommend_movie(self, ip_movie):
        all_movies = self.all_movie_list
        ans = []
        fans = {}
        exact_movie = self.fetch_exact_move(all_movies, ip_movie)
        exact_movie_bool = False
        if exact_movie:
            exact_movie_bool = True
            exact_cast = self.fetch_moves_credit_by_id(exact_movie['m_id'])
        fans['exact match'] = exact_movie
        fans['recommended_match'] = {}
        fans['recommended_match']['By Name'] = self.recommend_on_basis_of_name(all_movies, ip_movie, exact_movie_bool, exact_movie)
        if exact_movie_bool:
            fans['recommended_match']['By Genre'] = self.recommend_on_basis_of_genres(all_movies, ip_movie, exact_movie_bool, exact_movie)
        fans['recommended_match']['By Cast'] = []
        if exact_movie_bool:
            fans['recommended_match']['By Cast'] = self.recommend_on_basis_of_cast(all_movies, ip_movie, exact_movie_bool, exact_movie, exact_cast)
        fans['recommended_match']['final_show_to_user'] = []
        if exact_movie_bool:
            fans['recommended_match']['final_show_to_user'] = self.recommend_combined(fans['recommended_match']['By Name'], fans['recommended_match']['By Cast'], fans['recommended_match']['By Genre'])
        return fans

        
    def recommend_movie_multiple(self, ip_movie_list):
        all_movies = self.all_movie_list
        ans = []
        fans = {}
        exact_movie_list = self.fetch_exact_move_multiple(all_movies, ip_movie_list)
        exact_movie_bool = False
        if exact_movie_list:
            exact_movie_bool = True
            exact_cast_list = self.fetch_moves_credit_by_id_multiple(exact_movie_list)
        fans['exact match'] = exact_movie_list
        fans['recommended_match'] = {}
        fans['recommended_match']['By Name'] = self.recommend_on_basis_of_name_multiple(all_movies, ip_movie_list, exact_movie_bool, exact_movie_list)
        if exact_movie_bool:
            fans['recommended_match']['By Genre'] = self.recommend_on_basis_of_genres_multiple(all_movies, ip_movie_list, exact_movie_bool, exact_movie_list)
        if exact_movie_bool:
            fans['recommended_match']['By Cast'] = self.recommend_on_basis_of_cast_multiple(all_movies, ip_movie_list, exact_movie_bool, exact_movie_list, exact_cast_list)
        if exact_movie_bool:
            fans['recommended_match']['final_show_to_user'] = self.recommend_combined(fans['recommended_match']['By Name'], fans['recommended_match']['By Cast'], fans['recommended_match']['By Genre'])
        return fans

