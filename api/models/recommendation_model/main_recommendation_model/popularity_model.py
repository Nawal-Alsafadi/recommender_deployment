import numpy as np
import pandas as pd

from api.controllers.pandas_file_controller import PandasDf

number_of_product_ratings = "number_of_product_ratings"
average_product_rating = "average_product_rating"
product_ID = "productId"



# most popularity recommendation model
class PopularRecommendation:
    def __init__(self, train_data,user_column="userId", item_column="productId", rating_column="rating"):
        self.train_data = train_data
        self.filtered = None
        self.min_number_rating = None
        self.average_rating = None
        self.clear_data = False 
        self.user_column = user_column
        self.item_column = item_column
        self.rating_column = rating_column

    def read_data(self):
        data = PandasDf.read_csv(path=self.paths.popularityTrain)
        return data

    def read_results(self):
        data = PandasDf.read_csv(path=self.paths.popularityRecommendation)
        return data

    def weighted_score(self, x):
        v = x[number_of_product_ratings]
        R = x[average_product_rating]
        # Calculation based on an IMDB formula
        return (v / (v + self.min_number_rating) * R) + (
                self.min_number_rating / (self.min_number_rating + v) * self.average_rating)

    def create(self):
        self.train_data[number_of_product_ratings] = (
            self.train_data[self.item_column]
                .groupby(self.train_data[self.item_column])
                .transform("count")
        )
        # Create a column for the average rating a product has received called 'average_rating'
        self.train_data[average_product_rating] = (
            self.train_data[self.rating_column]
                .groupby(self.train_data[self.item_column])
                .transform("mean")
        )
        # Calculate the average rating for all products
        self.average_rating = self.train_data[self.rating_column].mean()
        # Calculate the minimum number of product ratings needs to receive in order to be included in the model
        self.min_number_rating = self.train_data[number_of_product_ratings].quantile(0.90)

        # Filter the dataSet based on value m
        self.filtered = self.train_data.copy().loc[
            self.train_data[number_of_product_ratings] >= self.min_number_rating
            ]
        # Create a 'score' column and give each product a weighted score
        self.filtered["score"] = self.filtered.apply(self.weighted_score, axis=1)
        self.filtered = self.filtered.sort_values("score", ascending=False)
        self.filtered = self.filtered.drop_duplicates(subset=self.item_column, keep="first")

        ## change the names 
        new_column_names = {self.item_column: 'productId', self.rating_column: 'ratings'}
        self.filtered= self.filtered.rename(columns=new_column_names)

        return self.filtered

    def recommend(self, user_id, num_recommendations=10):
        return self.filtered[
            [
                "productId",
                number_of_product_ratings,
                average_product_rating,
                "score",
            ]
        ].head(num_recommendations)
    
    def recommend_items(self,predictions_df: pd.DataFrame, num_recommendations=5):
        print("hola fro the func",self.item_column)

        # # Extracting the top recommendations based on popularity score
        # top_recommendations_indices = predictions_df.sort_values(by="score", ascending=False).head(num_recommendations)[self.item_column]
        results = predictions_df[
            [
                self.item_column,
                number_of_product_ratings,
                average_product_rating,
                "score",
            ]
        ].head(num_recommendations)

        # Converting the indices to a list of recommended item ids
        top_recommendations_item_ids =results[self.item_column].values.tolist()


        return top_recommendations_item_ids


class MostPopularRating:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

    def get_most_popular(self):
        self.data[number_of_product_ratings] = (
            self.data[self.item_column].groupby(self.data[self.item_column]).transform("count")
        )
        popular = self.data.sort_values(number_of_product_ratings, ascending=False)
        popular = popular.drop_duplicates(subset=self.item_column, keep="first")
        popular = popular[[self.item_column, number_of_product_ratings]]
        return popular.head(10)
