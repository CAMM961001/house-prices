import os

import numpy as np
import pandas as pd

from settings import Settings


# Initialize project settings
settings = Settings()



# Load feature selector
feature_selector = os.path.join(
    settings.ROOT_PATH,
    settings.CONFIG['assets']['feature_selector'])

feature_selector = pd.read_csv(feature_selector)

# Load train data to __file__
features = feature_selector.loc[feature_selector['consider'] == 1, 'feature']
train_data = settings.train_data[features.to_list()]



if __name__ == '__main__':
    print(train_data.info())