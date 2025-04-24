import pandas as pd
import matplotlib.pyplot as plt

input_csv_file = 'Datasets/Amazon/amazon_fashion.csv'

df = pd.read_csv(input_csv_file)

rating_counts = df['rating'].value_counts().sort_index() 
plt.bar(rating_counts.index, rating_counts.values, color='skyblue')

plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.title('Frequency of Ratings (1-5)')
plt.xticks(range(1, 6)) 

plt.show()

unique_books = df['asin'].nunique()
unique_users = df['user_id'].nunique()

print(f"Unique number of items: {unique_books}")
print(f"Unique number of users: {unique_users}")
print(f"Total number of rows in the dataset: {len(df)}")