import pandas as pd
df = pd.read_csv(
'csvFiles/yelp_review.csv',
header=0, 
index_col='review_id',
#index_col = 'business_id',
#names = ['business_id','name','neighborhood','address','city','state','postal_code','latitude','longitude','stars','review_count','is_open','categories'])
names=['review_id', 'user_id','business_id', 'stars', 'date', 'text', 'useful', 'funny', 'cool'])
df = df.sample(frac=0.02)
df.to_csv("csvFiles/review_mini.csv")
print("Sample CSV generated!")