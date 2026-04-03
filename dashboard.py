import streamlit as st
import pandas as pd
import os   

# Load data
# Load data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "listings.csv")

df = pd.read_csv(file_path)

# Clean price
df['price'] = df['price'].replace(r'[\$,]', '', regex=True)
df['price'] = pd.to_numeric(df['price'], errors='coerce')

st.set_page_config(layout="wide")

st.title("🏠 Airbnb Smart Pricing Advisor")

# Sidebar
st.sidebar.header("Filters")

room_type = st.sidebar.selectbox(
    "Select Room Type",
    df['room_type'].dropna().unique()
)

filtered_df = df[df['room_type'] == room_type]

# 🔥 KPI CARDS
col1, col2, col3 = st.columns(3)

col1.metric("Total Listings", len(filtered_df))
col2.metric("Average Price", round(filtered_df['price'].mean(), 2))
col3.metric("Max Price", int(filtered_df['price'].max()))

# 🔥 Recommendation
st.subheader("💡 Smart Pricing Insight")

overall_avg = df['price'].mean()
selected_avg = filtered_df['price'].mean()

st.write("Overall Market Avg:", round(overall_avg, 2))
st.write("Selected Category Avg:", round(selected_avg, 2))

if selected_avg > overall_avg:
    st.success("🔥 This listing is in a PREMIUM zone → You can price higher")
else:
    st.warning("💰 This listing is in a BUDGET zone → Keep price competitive")



    # 🔥 USER PRICE INPUT
st.subheader("💰 Check Your Listing Price")

user_price = st.number_input("Enter your price", min_value=0)

if user_price > 0:
    avg_price = filtered_df['price'].mean()

    st.write("Market Average:", round(avg_price, 2))

    if user_price > avg_price:
        st.error("❌ Your price is TOO HIGH (Overpriced)")
    elif user_price < avg_price:
        st.success("✅ Good deal! Your price is competitive")
    else:
        st.info("⚖️ Perfectly priced")

# 🔥 Chart
st.subheader("📊 Price by Location")

location_price = filtered_df.groupby('neighbourhood')['price'].mean()
st.bar_chart(location_price)

# 🔥 Top listings
st.subheader("🏆 Top Expensive Listings")

top_expensive = filtered_df.sort_values(by='price', ascending=False).head(5)
st.dataframe(top_expensive[['name', 'price']])



# 🔥 LOCATION FILTER
location = st.sidebar.selectbox(
    "Select Location",
    df['neighbourhood'].dropna().unique()
)

# Filter data based on both
filtered_df = df[
    (df['room_type'] == room_type) &
    (df['neighbourhood'] == location)
]

st.write("Unique locations:", df['neighbourhood'].nunique())


st.write("Unique neighbourhoods:", df['neighbourhood'].nunique())
st.write(df['neighbourhood'].value_counts().head(10))
