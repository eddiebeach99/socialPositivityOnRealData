import numpy as np
import pandas as pd
import modelSimAmazon as ms
import itertools
import matplotlib.pyplot as plt
import random

data_poor = pd.read_csv("C:/Users/edwar/SocialPositivityData/AmazonData/amazon_poor.csv")
data_rich = pd.read_csv("C:/Users/edwar/SocialPositivityData/AmazonData/amazon_rich.csv")

unique_products_rich = data_rich["asin"].unique()
df_filtered_rich = data_rich[data_rich["asin"].isin(unique_products_rich)]
unique_products_poor = data_poor["asin"].unique()
df_filtered_poor = data_poor[data_poor["asin"].isin(unique_products_poor)]


# Find 50 bandits that have at least 0.2 difference in average review recommendation
def filter_bandits(data):
    grouped = data.groupby('asin')
    item_recommendations = {asin: list(zip(group['rating'], group['user_id'])) for asin, group in grouped}

    ratings = {asin: [rating for rating, user_id in recs] for asin, recs in item_recommendations.items()}
    user_ids = {asin: [user_id for rating, user_id in recs] for asin, recs in item_recommendations.items()}
    
    bandit_a = []
    bandit_b = []
    conflicting_user_reviews = []
    conflicting_user_ids = []
    items_with_conflicts = []
    i = 0
    no_comparisons = 0
    
    for (item_id_a, recs_a), (item_id_b, recs_b) in (itertools.combinations(ratings.items(), 2)):
        i += 1
        if no_comparisons == 50:
            break
        if(item_id_a in items_with_conflicts or item_id_b in items_with_conflicts):
            continue
        if i % 1000000 == 0:
            print("Iterations: ", i)
        if np.abs(np.mean(recs_a) - np.mean(recs_b)) > 0.2:
            user_ids_a = user_ids[item_id_a]
            user_ids_b = user_ids[item_id_b]
            
            has_conflicting_user = False
            conflicting_user = None

            for user_id in set(user_ids_a).intersection(set(user_ids_b)):
                review_a = recs_a[user_ids_a.index(user_id)]
                review_b = recs_b[user_ids_b.index(user_id)]
                
                # Remove the reviews of the demonstrator for the bandits
                if (review_a == 1 and review_b == 0) or (review_a == 0 and review_b == 1):
                    has_conflicting_user = True
                    conflicting_user = user_id
                    
                    filtered_recs_a = [rating for idx, rating in enumerate(recs_a) if user_ids_a[idx] != conflicting_user]
                    filtered_recs_b = [rating for idx, rating in enumerate(recs_b) if user_ids_b[idx] != conflicting_user]
                    
                    # Ensure both lists still have at least 8 reviews
                    if len(filtered_recs_a) >= 8 and len(filtered_recs_b) >= 8:
                        items_with_conflicts.append(item_id_a)
                        items_with_conflicts.append(item_id_b)
                        bandit_a.append(filtered_recs_a)
                        bandit_b.append(filtered_recs_b)
                        conflicting_user_reviews.append([review_a, review_b])
                        conflicting_user_ids.append(conflicting_user)
                        no_comparisons += 1
                        print("Bandits found: ", no_comparisons)
            
            
            # If no conflicting user, skip to the next pair of items
            if not has_conflicting_user:
                continue
    
    
    bandits_amazon_poor = pd.DataFrame({
        'bandit_a': bandit_a,
        'bandit_b': bandit_b,
        'conflicting_user_reviews': conflicting_user_reviews
    })
    bandits_amazon_poor.to_csv("Simulation/Amazon/bandits_amazon_rich.csv", index=False)
    
    return bandit_a, bandit_b, conflicting_user_reviews

def simulation(file):
    np.random.seed(2025)
    bandit_data = pd.read_csv(file)
    
    bandit_a = [eval(x) for x in bandit_data['bandit_a']]
    bandit_b = [eval(x) for x in bandit_data['bandit_b']]
    conflicting_user_reviews = [eval(x) for x in bandit_data['conflicting_user_reviews']]
    
    all_pars = ms.param_gen(200000)
    result = ms.modelSim(all_pars, bandit_a, bandit_b, conflicting_user_reviews)
    
    result['bias'] = result.alpha1 - result.alpha2
    result.to_csv("C:/Users/edwar/SocialPositivityData/Amazon/simulation_amazon_rich.csv", index=False)


# Find out which bandits to use and then use the simulation function on them, don't forget to change the file names! 

# filter_bandits(df_filtered_rich)
simulation("Simulation/Amazon/bandits_amazon_rich.csv")
