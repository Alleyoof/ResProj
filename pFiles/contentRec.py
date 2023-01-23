import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel 
import time

startTime = time.process_time()
ds = pd.read_csv("../csvFiles/bmad_wis.csv")
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

def item(id):
    return ds.loc[ds['business_id'] == id]['name'].tolist()[0].split(' - ')[0]

# Just reads the results out of the dictionary.
def recommend(item_id, num):
    print("Recommending " + str(num) + " products similar to " + item(item_id) + "...")
    print("-------")
    v = results[item_id]
    filteredResults = [c for c in v if item(c[1]) != item(item_id)]
    recs = filteredResults[:num]
    for rec in recs:
        print("Recommended: " + item(rec[1]) + " (score:" + str(rec[0]) + ")")

# recommend(item_id='d5MXSInbPrPGK1lZxA3orQ', num=15)
print(f'Time: {time.process_time() - startTime:.3}s')