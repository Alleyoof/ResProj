import pandas as pd
from collabRec import makeCollab

test = pd.read_csv(
'../csvFiles/yTestmad_wis.csv',
header=0, 
# index_col='review_id',
# index_col = 'review_id',
#names = ['business_id','name','neighborhood','address','city','state','postal_code','latitude','longitude','stars','review_count','is_open','categories'])
names=['review_id', 'user_id','business_id', 'stars'])

train = pd.read_csv(
'../csvFiles/yTrainmad_wis.csv',
header=0, 
#index_col = 'business_id',
#names = ['business_id','name','neighborhood','address','city','state','postal_code','latitude','longitude','stars','review_count','is_open','categories'])
names=['review_id', 'user_id','business_id', 'stars'])

algo = makeCollab('Madison', 'Wisconsin', test=True)
myError = 0
dumbError = 0
predictDiff = []
amazingRecs = 0
dumbAmazRecs = 0
okRecs = 0
dumbOkRecs = 0
baselinish = 0
failures = 0
horrendousRecs = []
for v in test.index:
    # print(test)
    predRating = algo.predict(test.loc[v, 'user_id'], test.loc[v, 'business_id']).est
    origRating = test.loc[v, 'stars']
    predictDiff.append((abs(origRating-predRating), test.loc[v, 'business_id']))
    if abs(origRating-predRating) <= 0.3:
        amazingRecs += 1
    elif abs(origRating-predRating) <= 1:
        okRecs += 1
    elif abs(origRating-predRating) <= 2:
        baselinish += 1
    elif abs(origRating-predRating) > 3.5:
        horrendousRecs.append((origRating, predRating, 
        test.loc[v, 'business_id'], test.loc[v, 'user_id']))
    else:
        failures += 1
    if abs(origRating-3) <= 0.3:
        dumbAmazRecs += 1
    elif abs(origRating-3) <= 1:
        dumbOkRecs += 1
    myError += ((origRating - predRating) ** 2)
    dumbError += ((origRating - 3) ** 2)


predictDiff.sort()
print(f'Model error: {myError}')
print(f'Dumb error: {dumbError}')
print(f'Amazing Recs(dumb): {dumbAmazRecs}')
print(f'Amazing Recs(Model): {amazingRecs}')
print(f'Good Recs(dumb): {dumbOkRecs}')
print(f'Good Recs(Model): {okRecs}')
print(f'Baseline: {baselinish}')
print(f'Failures: {failures}')
print(f'Terrible failures: {len(horrendousRecs)}')
print(f'Total Recs: {len(test.index)}')


# print(predictDiff)
