from surprise import Dataset
from surprise import Reader
from surprise import KNNWithMeans
import pandas as pd
import time
from csv import reader

startTime = time.process_time()
with open('C:\\Users\\vpjon\\OneDrive\\Documents\\Research Project\\csvFiles\\yelpmad_wis.csv', 'r', encoding="utf-8") as file:
    data = list(reader(file))
initDict = { 
    # userID : [[business, rating]]
}

myVals = {
    "user" : [],
    "business": [],
    "rating": [] 
} 

trainDataSize = len(data)
# note -> collaboratie recommender only uses first 10k reviews
for v in data[1:trainDataSize]: # v[0] => user id
    myVals["user"].append(v[1])
    myVals["business"].append(v[2])
    myVals["rating"].append(int(v[3]))

df = pd.DataFrame(myVals)
reader = Reader(rating_scale=(1, 5))

data = Dataset.load_from_df(df[["user", "business", "rating"]], reader)
# Loads the builtin Movielens-100k data
# movielens = Dataset.load_builtin('ml-100k')

sim_options = {
    "name": "cosine",
    "user_based": False,  # Compute  similarities between items
}

algo = KNNWithMeans(sim_options=sim_options)

# print("Building training set...")
trainingSet = data.build_full_trainset() # build set

# print("Fitting set...")
algo.fit(trainingSet)

#prediction = algo.predict("PzaOWDZjtxrrAhdv8PM6cQ", 'ugDCPgJUCRuNpHSPsMZwk') # make prediction, userid, itemid
#print(prediction.est)
print(f'Collab reccomender generated in {(time.process_time() - startTime):.3}s')