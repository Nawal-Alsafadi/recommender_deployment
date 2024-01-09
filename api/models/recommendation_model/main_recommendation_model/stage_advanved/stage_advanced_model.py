# import pandas as pd
# import numpy as np
# from pandas import DataFrame
# from scipy.sparse.linalg import svds
# from api.controllers.pandas_file_controller import PandasDf
# from db_connection import db
# from api.utils.paths import Paths


# class CollaborativeRecommendation:
#     def __init__(self):
#         self.paths = Paths()
#         self.utility_matrix = None
#         self.predicted_ratings = None

#     def read_data(self):
#         data = PandasDf.read_csv(path=self.paths.collaborativeTraining)
#         return data

#     def read_results(self):
#         data = PandasDf.read_csv(path=self.paths.collaborativeRecommendation)
#         return data

#     # Training the model
#     def train(self, data: DataFrame):
#         self.utility_matrix = data.pivot(index='userId', columns='productId', values='rating').fillna(0)
#         predictions_df = self._calculate_predictions(k=20)
#         return predictions_df

#     def save_results(self, predictions_df: DataFrame, clear_data: bool):
#         collaborative = db.collaborative
#         # PandasDf.write_csv(path=self.paths.collaborativeRecommendation, df=predictions_df, index=True)
#         '''save result to db'''
#         import time
#         start_time = time.time()

#         def sort_similarities(row, columns):
#             values = row.values
#             sorted_indices = values.argsort()[::-1]
#             doc = {"_id": row.name, "products": list(
#                 map(lambda ind: {"product_id": int(columns[ind]), "similarity": values[ind]}, sorted_indices)),
#                    }
#             if clear_data:
#                 return doc
#             collaborative.update_one({"_id": row.name}, {"$set": doc}, upsert=True)
#             return None

#         series = predictions_df.apply(lambda x: sort_similarities(row=x, columns=predictions_df.columns),
#                                       axis=1)
#         docs = series.values.tolist()
#         if clear_data:
#             collaborative.delete_many({})
#             collaborative.insert_many(docs)
#         end_time = time.time()
#         print(f"estimated time {end_time - start_time}")

#     def _calculate_predictions(self, k=20):
#         u, sigma, vt = svds(self.utility_matrix.values, k=k)
#         sigma = np.diag(sigma)
#         predicted_ratings = np.dot(np.dot(u, sigma), vt)
#         user_ids = self.utility_matrix.index
#         product_ids = self.utility_matrix.columns
#         predictions_df = pd.DataFrame(predicted_ratings, index=user_ids, columns=product_ids)
#         return predictions_df

#     def initialize_collaborative_model(self):
#         pass

#     # get recommendations
#     @staticmethod
#     def recommends(user_id, num_recommendations):
#         collection = db.collaborative

#         '''first way but we prefer aggregation to get cleaned data'''
#         '''projection = {'_id': 0, 'products': {'$slice': num_recommendations}}
#         document = collection.find_one({'_id': user_id}, projection)
#         return document'''

#         '''aggregate'''
#         docs = collection.aggregate([
#             {"$match": {"_id": user_id}},
#             {"$project": {"_id": 0, 'products': {'$slice': ["$products", num_recommendations]}}},
#             {"$unwind": "$products"},
#             {
#                 "$project": {
#                     "product_id": "$products.product_id",
#                     # "similarity": "$similar_products.similarity",
#                 }
#             }
#         ])
#         return list(map(lambda doc: doc["product_id"], docs))
