import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel 
import time

def makeContent(myCity, myState, categories):
    # print()
    # print(categories)
    startTime = time.process_time()
    ds = pd.read_csv(f"../csvFiles/b{myCity.lower()[:3]}_{myState.lower()[:3]}.csv")
    # the below code adds a dummy data point that holds the needed categories(done out of laziness lol)
    ds.loc[len(ds)-1] = ["addedCategory", "d", "d", "d", "d", "d", "d", "d", ";".join(categories)]
    # print(ds.loc[len(ds)-1])
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(ds['categories'])

    # generate cos similarity matrix
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    results = {}    

    for idx, row in ds.iterrows():
        # get first 100 items
        similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
        similar_items = [(cosine_similarities[idx][i], ds['business_id'][i]) for i in similar_indices]
        results[row['business_id']] = similar_items[1:]
    
    print('Content based recommender generated!')
    print(f'Time: {time.process_time() - startTime:.3}s')
    return ds, results

def item(ds, id):
    name = ds.loc[ds['business_id'] == id]['name'].tolist()[0].split(' - ')[0]
    address = ds.loc[ds['business_id'] == id]['address'].tolist()[0].split(' - ')[0]
    stars = ds.loc[ds['business_id'] == id]['stars'].tolist()[0]
    # print(address)
    return [name[1:-1], address[1:-1], stars]

# Just reads the results out of the dictionary.
def recommend(ds, results, item_id, num):
    print("Recommending " + str(num) + " places")
    print("-------")
    v = results[item_id]
    # print(v)
    filteredResults = [c for c in v if item(ds, c[1]) != item(ds, item_id)]
    # print(filteredResults)
    # recs = filteredResults[:num]
    results = []
    resNames = []
    count = 0
    for rec in filteredResults:
        if count >= num:
            break
        if item(ds, rec[1])[0] not in resNames:
            count += 1
            results.append((*item(ds, rec[1]), str(rec[0] * 100)))
            resNames.append(item(ds,rec[1])[0])
        # print("Recommended: " + item(ds, rec[1]) + " (score:" + str(rec[0]) + ")")
    return results

# myDs, myResults = makeContent('Madison', 'Wisconsin', ['Ice Cream & Frozen Yogurt'])
# print(recommend(myDs, myResults, item_id='addedCategory', num=15))
