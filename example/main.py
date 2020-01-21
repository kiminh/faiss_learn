import faiss
import numpy
from scipy.sparse import coo_matrix
from sklearn.decomposition import NMF
from flask import Flask, jsonify

# constants
RANDOM_STATE = 0
N_FACTOR = 20
N_RESULT = 10

# load dataset
# tuple array
ratings = numpy.loadtxt(
    'movielens-small/ratings.csv',
    delimiter=',',
    skiprows=1,
    usecols=(0, 1, 2),
    dtype=[('userId', 'i8'), ('movieId', 'i8'), ('rating', 'f8')],
)

data = ratings['rating']
users = sorted(numpy.unique(ratings['userId']))  # list
movies = sorted(numpy.unique(ratings['movieId']))  # list

# for later use
user_id2i = {id: i for i, id in enumerate(users)}  # map user id to index
movie_id2i = {id: i for i, id in enumerate(movies)}  # map movie id to index
movie_i2id = {i: id for i, id in enumerate(movies)}  # map movie index to id

row = list(map(user_id2i.get, users))
col = list(map(movie_id2i.get, movies))
# user_movie = (users, movies)  # user and movie map

print(len(users))
print(len(movies))

# make sparse matrix
rating_mat = coo_matrix((data, (row, col)), shape=(2, 2))

# # decompose
# model = NMF(n_components=N_FACTOR, init='random', random_state=RANDOM_STATE)
# user_mat = model.fit_transform(rating_mat)
# movie_mat = model.components_.T
#
# # indexing
# movie_index = faiss.IndexFlatIP(N_FACTOR)
# movie_index.add(movie_mat.astype('float32'))
#
# # create app
# # app = Flask(__name__)
#
#
# # API endpoint
# # @app.route('/user/<int:user_id>')
# def users(user_id):
#     user_i = user_id2i[user_id]
#     user_vec = user_mat[user_i].astype('float32')
#     scores, indices = movie_index.search(numpy.array([user_vec]), N_RESULT)
#     movie_scores = zip(indices[0], scores[0])
#     return jsonify(
#         movies=[
#             {
#                 "id": int(movie_i2id[i]),
#                 "score": float(s),
#             }
#             for i, s in movie_scores
#         ],
#     )
#
#
# # app.run(host="0.0.0.0", port=5000)
#
# users(1)
