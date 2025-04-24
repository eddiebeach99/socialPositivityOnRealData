import pandas as pd
import matplotlib.pyplot as plt

# Input CSV file path
input_csv_file = 'Datasets/Bookreads/goodreads_reviews_poetry.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(input_csv_file)

# Plot the frequency of ratings
rating_counts = df['rating'].value_counts().sort_index()  # Count frequency of each rating and sort by rating
plt.bar(rating_counts.index, rating_counts.values, color='skyblue')

# Add labels and title
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.title('Frequency of Ratings (1-5)')
plt.xticks(range(1, 6))  # Ensure x-axis shows ratings from 1 to 5

# Show the plot
plt.show()

# Calculate and print the unique number of books and users
unique_books = df['book_id'].nunique()
unique_users = df['user_id'].nunique()

print(f"Unique number of books: {unique_books}")
print(f"Unique number of users: {unique_users}")
print(f"Total number of rows in the dataset: {len(df)}")