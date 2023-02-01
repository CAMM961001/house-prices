import pandas as pd
import datetime as dt

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score

from time import process_time
from settings import Settings


# Initialize project settings
settings = Settings()

# Get target name
target = settings.target

# Load processed train data to __file__
train = settings.processed_train

# Split in features and target
X = train.drop(columns=target)
y = train[target].values.ravel()

# Hyper-parameters
max_leaf_nodes = settings.CONFIG['model']['max_leafs']
n_folds = settings.CONFIG['model']['n_folds']

# Train model
start = process_time()

model = RandomForestRegressor(max_leaf_nodes=max_leaf_nodes)
model.fit(X=X, y=y)
scores = cross_val_score(model, X, y, cv=n_folds)

stop = process_time()

# Predict


if __name__ == '__main__':

    # Register task in log file
    # log = os.path.join(settings.ROOT_PATH, settings.CONFIG['assets']['pipe_log'])
    
    prompt = f"Job: {__file__}\n"
    prompt += "Status: DONE\n"
    prompt += f"TimeStamp: {dt.datetime.now()}\n"
    prompt += f"Scores: {scores}\n"
    prompt += f"MeanScore: {scores.mean()}\n"
    prompt += f"ProcessTime: {stop - start} [seconds]"

    # with open(file=log, mode='a') as f:
    #     f.write(prompt)
    # f.close()

    print(prompt)