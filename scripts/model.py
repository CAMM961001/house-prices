import os, sys
import logging

import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score

from time import process_time
from settings import Settings


# Initialize project settings
settings = Settings()

# Get target name
target = settings.target

# Load processed data data to __file__
try:
    train = settings.invoque_data('processed_train')
    test = settings.invoque_data('processed_test')

except FileNotFoundError:
    # Exception prompt
    prompt = f'An exception has occurred, either:\n'
    prompt += f'\t- "{settings.CONFIG["assets"]["processed_train"]}" or\n'
    prompt += f'\t- "{settings.CONFIG["assets"]["processed_test"]}" '
    prompt += 'not found in assets dir\n'
    
    # Add prompt to log file
    logging.error(prompt)
    sys.exit(1)

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
sale_price = model.predict(test)
predictions_df = pd.DataFrame({
    "Id": test.index + 1,
    "SalePrice": sale_price
})

# Save predictions to csv
settings.save_df(df=predictions_df, env_var='predictions')


if __name__ == '__main__':

    # Register task in log file
    prompt = f"Job in {__file__}:\n"
    prompt += "\t- Status: DONE\n"
    prompt += f"\t- MeanScore: {scores.mean()}\n"
    prompt += f"\t- TrainTime: {stop - start} [seconds]\n"

    # Add prompt to log file
    logging.info(prompt)