import pandas as pd

# Load dataset
df = pd.read_csv("data/listings.csv")

# Show original price
print("Before cleaning:")
print(df['price'].head())

# Remove $ and commas
df['price'] = df['price'].replace('[\$,]', '', regex=True)

# Convert to numeric
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Show cleaned price
print("\nAfter cleaning:")
print(df['price'].head())
print("\nAverage Price:", df['price'].mean())
# Average price by room type
room_price = df.groupby('room_type')['price'].mean()

print("\nAverage Price by Room Type:")
print(room_price)
# Top 5 most expensive listings
top_expensive = df.sort_values(by='price', ascending=False).head(5)

print("\nTop 5 Expensive Listings:")
print(top_expensive[['name', 'price', 'room_type']])



# Average price by neighborhood
location_price = df.groupby('neighbourhood')['price'].mean().sort_values(ascending=False)

print("\nAverage Price by Location:")
print(location_price)


import matplotlib.pyplot as plt

# Bar chart for location price
location_price.head(10).plot(kind='bar')

plt.title("Top 10 Expensive Locations")
plt.xlabel("Location")
plt.ylabel("Average Price")

plt.show()

print("\nAll Locations:")
print(location_price)

print("\nMost Expensive Location:", location_price.idxmax())
print("Cheapest Location:", location_price.idxmin())