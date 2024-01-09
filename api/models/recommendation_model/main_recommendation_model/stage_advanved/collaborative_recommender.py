import pandas as pd

import numpy as np
import surprise
from pandas import DataFrame
from api.controllers.pandas_file_controller import PandasDf
from api.utils.paths import Paths


class CollaborativeRecommender: 
    def __init__(self ,user_column='userID', item_column='movieID', rating_column='rating'):
        self.paths = Paths()
        self.clear_data = False 
        self.user_column = user_column
        self.item_column = item_column
        self.rating_column = rating_column

    def read_data(self,csv_path):
        data = PandasDf.read_csv(path=csv_path)
        return data

    def read_results(self):
        data = PandasDf.read_csv(path=self.paths.collaborativeRecommendation)
        return data


    def compute_predictions(self, algo, data: DataFrame, remove_seen=True):
        preds_lst = []
        users = data[self.user_column].unique()
        items = data[self.item_column].unique()
        for user in users:
            for item in items:
                preds_lst.append([user, item, algo.predict(user, item).est])
        predictions = pd.DataFrame(data=preds_lst, columns=[self.user_column, self.item_column, 'prediction'])
        if remove_seen:
            tempdf = pd.concat([data[[self.user_column, self.item_column]],pd.DataFrame(data=np.ones(data.shape[0]), columns=["dummycol"], index=data.index), ],axis=1, )
            merged = pd.merge(tempdf, predictions, on=[self.user_column, self.item_column], how="outer")
            predictions = merged[merged["dummycol"].isnull()].drop("dummycol", axis=1)
        predictions = predictions.pivot(index=self.user_column, columns=self.item_column, values='prediction')
        return predictions

    def prepare_data(self, data: DataFrame):
        new_data = data.loc[:, [self.user_column, self.item_column, self.rating_column]]
        train_set = surprise.Dataset.load_from_df(new_data, reader=surprise.Reader('ml-1m')).build_full_trainset()
        return train_set, new_data

    def train(self, data: DataFrame):
        train_set, new_data = self.prepare_data(data)
        svd = surprise.SVD(random_state=0, n_factors=200, n_epochs=30)
        svd.fit(train_set)
        predictions_df = self.compute_predictions(svd, new_data)
        return predictions_df

    def save_results(self, predictions_df: DataFrame):
        PandasDf.write_csv(path=self.paths.collaborativeRecommendation, df=predictions_df, index=False)

    @staticmethod
    def recommend_items(user_id, predictions: DataFrame, num_recommendations=5):
        user_id = int(user_id)
        user_predictions = predictions.loc[user_id]
        top_recommendations_indices = user_predictions.sort_values(ascending=False).head(num_recommendations).index
        top_recommendations_movie_ids = top_recommendations_indices.tolist()
        return top_recommendations_movie_ids



