import pandas as pd
from cityStateCSV import createCSV
import os
import string, random
import numpy as np

# the following are methods that add, delete, and find reviews
def findAdd(address, myCity, myState, userID, rating):
    if not os.path.exists(f'../csvFiles/y{myCity.lower()[:3]}_{myState.lower()[:3]}.csv'):
        createCSV(myCity=myCity, myState=myState)
    dfrev = pd.read_csv(f'../csvFiles/y{myCity.lower()[:3]}_{myState.lower()[:3]}.csv',
    header=0, 
    names=['review_id', 'user_id','business_id', 'stars'],
    dtype={'stars': int},
    index_col= 'review_id'
    )
    #print(dfrev.dtypes)
    dfbusi = pd.read_csv(f'../csvFiles/b{myCity.lower()[:3]}_{myState.lower()[:3]}.csv',
    header=0, 
    names = ['business_id','name','address','city','state','latitude','longitude','stars','categories'],
    index_col= False
    )

    # fix the below code, find the id of business based on location
    # perhaps switch to lat, long (similar to findLocAndRec)
    business = dfbusi[dfbusi['address'] == f'\"{address}\"']
    if len(business['business_id']) == 0:
        print("Invalid values")
        return -1 
    myBusiId = business['business_id'].iloc[0]
    #print(myBusiId)
    myReviewid = randomword(18)
    dfrev.loc[myReviewid] = [userID, myBusiId, rating] 
    dfrev.to_csv(f'../csvFiles/y{myCity[:3].lower()}_{myState[:3].lower()}.csv')

def findDel(name, address, myCity, myState, userID, rating):
    if not os.path.exists(f'../csvFiles/y{myCity.lower()[:3]}_{myState.lower()[:3]}.csv'):
        print('No reviews to delete')
        return
    dfrev = pd.read_csv(f'../csvFiles/y{myCity.lower()[:3]}_{myState.lower()[:3]}.csv',
    header=0, 
    names=['review_id', 'user_id','business_id', 'stars'],
    dtype={'stars': int},
    index_col= 'review_id'
    )
    #print(dfrev.dtypes)
    dfbusi = pd.read_csv(f'../csvFiles/b{myCity.lower()[:3]}_{myState.lower()[:3]}.csv',
    header=0, 
    names = ['business_id','name','address','city','state','latitude','longitude','stars','categories'],
    index_col= False
    )

    business = dfbusi[(dfbusi['address'] == f'\"{address}\"') & (dfbusi['name'] == f'\"{name}\"')]
    # print(business)
    myBusiId = business['business_id'].iloc[0]
    # print(myBusiId)
    dfrev = dfrev[(dfrev['user_id'] != userID) | (dfrev['business_id'] != myBusiId)]
    dfrev.to_csv(f'../csvFiles/y{myCity[:3].lower()}_{myState[:3].lower()}.csv')

def getReviews(userID, myCity, myState):
    if not os.path.exists(f'../csvFiles/y{myCity.lower()[:3]}_{myState.lower()[:3]}.csv'):
        print('No reviews to find.')
        return -1
    dfrev = pd.read_csv(f'../csvFiles/y{myCity.lower()[:3]}_{myState.lower()[:3]}.csv',
    header=0, 
    names=['review_id', 'user_id','business_id', 'stars'],
    dtype={'stars': int},
    index_col= False)

    dfbusi = pd.read_csv(f'../csvFiles/b{myCity.lower()[:3]}_{myState.lower()[:3]}.csv',
    header=0, 
    names = ['business_id','name','address','city','state','latitude','longitude','stars','categories'],
    index_col= False)

    listOfReviews = [] # tuple with address & rating
    myReviews = dfrev[dfrev['user_id'] == userID]
    if len(myReviews) == 0:
        print('No reviews for user')
        return -1
    for i, v in enumerate(myReviews['business_id']):
        myRow = dfbusi[dfbusi['business_id'] == v]
        name = myRow['name'].iloc[0]
        address = myRow['address'].iloc[0]
        rating = myReviews['stars'].iloc[i]
        listOfReviews.append((name[1:-1], address[1:-1], rating))
        # add to listofreviews
    # print(listOfReviews)
    return listOfReviews

def randomword(length):
   letters = string.ascii_lowercase
   return 'NEW:' + ''.join(random.choice(letters) for i in range(length))

# findAdd('32 W Towne Mall', 'Madison', 'Wisconsin', 'lwkhnfwejioi32423798', 5)
# findAdd('2302 Packers Ave', 'Madison', 'Wisconsin', 'lwkhnfwejioi32423798', 4)
# findAdd('111 N Broom St', 'Madison', 'Wisconsin', 'lwkhnfwejioi32423798', 3)

# findAdd('581 Howe Ave', 'Cuyahoga Falls', 'Ohio', 'lwkhnfwejioi32423798', 4)
# findDel('32 W Towne Mall', 'Madison', 'Wisconsin', 'lwkhnfwejioi32423798', 4)
# getReviews('KoY4KGxev8gdg5qQpyDlZA', 'Madison', 'Wisconsin')
