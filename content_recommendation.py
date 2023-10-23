import pandas as pd
import numpy as np
from pydantic import BaseModel

# Import CountVectorizer create the count matrix
from sklearn.feature_extraction.text import CountVectorizer
# Compute the Cosine Similarity matrix based on the count_matrix
from sklearn.metrics.pairwise import cosine_similarity

# Importing db of food items across all canteens registered on the platform
df1 = pd.read_csv('./meta_mart_db/food.csv')
df1.columns = ['id', 'name', 'description', 'imageUrl', 'productSize', 'file', 'price', 'quantity', 'currency', 'type', 'createdAt', 'updatedAt', 'isDiscounted', 'discountedPrice', 'subType']


# TODO: clean data

# Creating soup string for each item
def create_soup(x):
    tags = x['name'].lower().split(', ')
    tags.extend(x['type'].lower().split())
    tags.extend(x['subType'].lower().split())
    return " ".join(sorted(set(tags), key=tags.index))



df1['soup'] = df1.apply(create_soup, axis=1)

# create the count matrix
count = CountVectorizer(stop_words='english')

# df1['soup']
count_matrix = count.fit_transform(df1['soup'])

# Compute the Cosine Similarity matrix based on the count_matrix
cosine_sim = cosine_similarity(count_matrix, count_matrix)

indices_from_title = pd.Series(df1.index, index=df1['name'])
indices_from_food_id = pd.Series(df1.index, index=df1['id'])


# Function that takes in food title or food id as input and outputs most similar dishes
def get_recommendations(title="", cosine_sim=cosine_sim, idx=-1):
    # Get the index of the item that matches the title
    if idx == -1 and title != "":
        idx = indices_from_title[title]

    # Get the pairwsie similarity scores of all dishes with that dish
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the dishes based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar dishes
    sim_scores = sim_scores[1:3]

    # Get the food indices
    food_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar dishes
    return df1.loc[food_indices]


class FoodRecommendationResponse(BaseModel):
    recommendations: list