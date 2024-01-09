import pandas as pd
import numpy as np
import surprise
from pandas import DataFrame
from api.controllers.pandas_file_controller import PandasDf
from sklearn.metrics.pairwise import cosine_similarity
from api.models.recommendation_model.main_recommendation_model.stage_advanved.collaborative_recommender import CollaborativeRecommender
from api.utils.paths import Paths


class HybridRecommender:
    def __init__(self,user_column='userID', item_column='movieID', rating_column='rating',attribute_column = 'genres'):
        self.paths = Paths()
        self.features = None
        # self.collaborative_recommender = CollaborativeRecommender()
        self.clear_data = False 
        self.user_column = user_column
        self.item_column = item_column
        self.rating_column = rating_column
        self.attribute_column = attribute_column

    def read_data(self,csv_path):
        data = PandasDf.read_csv(path=csv_path)
        return data

    def read_results(self):
        data = PandasDf.read_csv(path=self.paths.hybridResults)
        data = data.set_index('userID')
        return data

    def build_profiles(self, data: DataFrame):
        genres = list(set([x for genres in data[self.attribute_column].values for x in genres.split('|')]))
        for g in genres:
            data[g] = [0 if not g in genres.split('|') else 1 for genres in data[self.attribute_column].values]
        self.features = data.columns[5:]
        user_profiles = data.groupby(self.user_column)[self.features].mean().reset_index()
        item_profiles = data.groupby(self.item_column)[self.features].mean().reset_index()
        return user_profiles, item_profiles

  
    def calculate_similarity_matrix(self, user_profiles, item_profiles):
        user_profiles_values = user_profiles.iloc[:, 1:].values
        item_profiles_values = item_profiles.iloc[:, 1:].values
        similarity_matrix = cosine_similarity(user_profiles_values, item_profiles_values)
        similarity_df = pd.DataFrame(similarity_matrix, index=user_profiles[self.user_column], columns=item_profiles[self.item_column])
        return similarity_df
    def train(self, data: DataFrame):
        user_profiles, item_profiles = self.build_profiles(data)
        similarity_df = self.calculate_similarity_matrix( user_profiles, item_profiles)
        return similarity_df

    def save_results(self, similarity_df: DataFrame):


        new_column_names = {self.user_column: 'userID'}
        similarity_df= similarity_df.rename(columns=new_column_names)
        similarity_df = similarity_df.rename_axis(index={self.user_column: 'userID'})
        PandasDf.write_csv(path=self.paths.hybridResults, df=similarity_df, index=True)

    @staticmethod
    def hybrid_recommendes(similarity_matrix, user_id, item_list, num_recommendations=5):
        user_similarity_scores = similarity_matrix.loc[user_id]
        filtered_item_list = [item for item in item_list if item in user_similarity_scores.index]
        sorted_items = sorted(filtered_item_list, key=lambda x: user_similarity_scores[x], reverse=True)
        top_n_items = sorted_items[:num_recommendations]
        return top_n_items