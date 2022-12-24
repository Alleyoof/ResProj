import pandas as pd
import time
sTime = time.process_time()
df = pd.read_csv(
'C:\\Users\\vpjon\\OneDrive\\Documents\\Research Project\\pFiles\\yelp_business.csv',
header=0, 
#index_col='review_id',
index_col = 'business_id',
names = ['business_id','name','neighborhood','address','city','state','postal_code','latitude','longitude','stars','review_count','is_open','categories'])
#names=['review_id', 'user_id','business_id', 'stars', 'date', 'text', 'useful', 'funny', 'cool'])
myCity = 'Madison'
myState = 'Wisconsin'
df = df[df.isin([myCity]).any(axis=1)]
businessIds = []
#names=['review_id', 'user_id','business_id', 'stars', 'date', 'text', 'useful', 'funny', 'cool'])
def func(x):
    businessIds.append(x.name)
    # else:  
    #     print(x)
    #add selenium code
df.apply(func, axis=1)
df.to_csv(f'csvFiles/b{myCity[:3].lower()}_{myState[:3].lower()}.csv')
print("Mad wis Business CSV generated!")
# separate business csv and yelp csv
df = pd.read_csv(
'C:\\Users\\vpjon\\OneDrive\\Documents\\Research Project\\csvFiles\\yelp_review.csv',
header=0, 
index_col='review_id',
names=['review_id', 'user_id','business_id', 'stars', 'date', 'text', 'useful', 'funny', 'cool'])
df = df[df['business_id'].isin(businessIds)]
df.to_csv(f'csvFiles/y{myCity[:3].lower()}_{myState[:3].lower()}.csv')
print("Reviews csv generated")
print(f'Time: {time.process_time() - sTime}s')