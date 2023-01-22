import pandas as pd
import time

def createCSV(myCity, myState):
    sTime = time.process_time()
    df = pd.read_csv(
    'csvFiles/yelp_business.csv',
    header=0, 
    #index_col='review_id',
    index_col = 'business_id',
    names = ['business_id','name','neighborhood','address','city','state','postal_code','latitude','longitude','stars','review_count','is_open','categories'])
    df = df[df.isin([myCity]).any(axis=1)]
    businessIds = []
    #names=['review_id', 'user_id','business_id', 'stars', 'date', 'text', 'useful', 'funny', 'cool'])
    def func(x):
        businessIds.append(x.name)
    df.apply(func, axis=1)
    del df['neighborhood']
    del df['postal_code']
    del df['review_count']
    del df['is_open']
    df.to_csv(f'csvFiles/b{myCity[:3].lower()}_{myState[:3].lower()}.csv')
    print("Mad wis Business CSV generated!")
    # separate business csv and yelp csv
    df = pd.read_csv(
    'csvFiles/yelp_review.csv',
    header=0, 
    index_col='review_id',
    names=['review_id', 'user_id','business_id', 'stars', 'date', 'text', 'useful', 'funny', 'cool'])
    df = df[df['business_id'].isin(businessIds)]
    del df['date']
    del df['text']
    del df['useful']
    del df['funny']
    del df['cool']
    df.to_csv(f'csvFiles/y{myCity[:3].lower()}_{myState[:3].lower()}.csv')
    print("Reviews csv generated")
    print(f'Time: {time.process_time() - sTime}s')
# createCSV('Madison', 'Wisconsin')