
import sqlite3
import pandas as pd
import numpy as np
import json
#recommendations =

conn = sqlite3.connect("mf.sqlite3")
movies = pd.read_sql_query("select title, poster_path, runtime, genres, vote_average, vote_count from movies", conn)
c = movies['vote_average'].mean()
m = movies['vote_count'].quantile(0.9)


def wrdf():

	q_movies = movies.copy().loc[movies['vote_count'] >= m]
	q_movies['score'] = q_movies.apply(weighted_rating, axis=1)
	q_movies = q_movies.sort_values('score', ascending=False)
	return q_movies[['title', 'poster_path','runtime','genres','vote_count', 'vote_average', 'score']]

def weighted_rating(x, m=m, c=c):
    v = x['vote_count']
    R = x['vote_average']
    # Calculation based on the IMDB formula
    return (v/(v+m) * R) + (m/(m+v) * c)

from collections import defaultdict
def get_top_n(predictions, n=10):
    # First map the predictions to each user.
    top_n = defaultdict(list)
    print(top_n)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n

from surprise import Reader, Dataset, SVD, model_selection
from surprise.model_selection import cross_validate
def collaborative():
	conn = sqlite3.connect("mf.sqlite3")
	movies = pd.read_sql_query("select title, poster_path, runtime, genres, vote_average, vote_count from movies", conn)
	ratings = pd.read_sql_query("select * from ratings", conn)
	reader = Reader()
	data = Dataset.load_from_df(ratings[['userid', 'movieid', 'rating']],reader= reader)
	svd=SVD()
	cross_validate(svd, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
	trainset = data.build_full_trainset()
	print(trainset)
	testset = trainset.build_anti_testset()
	predictions = svd.test(testset)

	top_n = get_top_n(predictions, n=10)

	# Print the recommended items for each user
	recommendations = {}
	for uid, user_ratings in top_n.items():
		recommendations[uid] = [iid for(iid, _) in user_ratings]
	with open('catalog/output.py', 'w') as filehandle:
		filehandle.write('recommendations=') 
		filehandle.write(json.dumps(recommendations))
		
	return recommendations

	
