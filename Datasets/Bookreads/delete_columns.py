import pandas as pd

# Load your dataset (replace 'your_file.csv' with your actual file)
df = pd.read_csv("C:/Users/edwar/SocialPositivityData/GoodreadsData/goodreads_poor.csv")



# Shuffle the dataset randomly
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save the modified dataset (optional)
df.to_csv("C:/Users/edwar/SocialPositivityData/GoodreadsData/goodreads_poor.csv", index=False)