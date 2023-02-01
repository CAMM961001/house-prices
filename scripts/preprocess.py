import os

import numpy as np
import pandas as pd
import datetime as dt

from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
from settings import Settings


def encode_data(df, ord, cat):
    """
    
    """
    # Ordinal encoding
    for feat in ord:
        feat_order = feat_select.loc[feat_select['feature'] == feat, 'order']
        feat_order = feat_order.values[0].split(";")

        ord_enc = OrdinalEncoder(
            categories=[feat_order],
            handle_unknown='use_encoded_value',
            unknown_value=-1)
        ord_enc = ord_enc.fit_transform(df[[feat]])
        df.loc[df.index, feat] = ord_enc


    # One hot encoding
    for feat in cat:
        ohe = OneHotEncoder(
            sparse_output=False,
            handle_unknown='infrequent_if_exist')
        
        ohe = pd.DataFrame(
            ohe.fit_transform(df[[feat]]),
            columns=ohe.get_feature_names_out())

        df = df.join(ohe)
        df.drop(columns=feat, inplace=True)

    return df


# Initialize project settings
settings = Settings()

# Load feature selector data
feat_select = os.path.join(
    settings.ROOT_PATH,
    settings.CONFIG['assets']['feature_selector'])

feat_select = pd.read_csv(feat_select)
feat_select = feat_select.loc[feat_select['consider'] != 0]

# List of numerical, categorical and ordinal features
num = feat_select.loc[feat_select['type_class'] == 'numerical']
num = num['feature'].to_list()

cat = feat_select.loc[feat_select['type_class'] == 'categorical']
cat = cat['feature'].to_list()

ord = feat_select.loc[feat_select['type_class'] == 'ordinal']
ord = ord['feature'].to_list()

# Load desired features from train data to __file__
train_data = settings.train_data[feat_select['feature'].to_list()]
train_data = encode_data(df=train_data, ord=ord, cat=cat)

# Load desired features from test data to __file__
test_data = feat_select.loc[feat_select['consider'] == 1]['feature'].to_list()
test_data = settings.test_data[test_data]
test_data = encode_data(df=test_data, ord=ord, cat=cat)

if __name__ == '__main__':

    # Save processed data in assets directory
    processed_train = os.path.join(
        settings.ROOT_PATH,
        settings.CONFIG['assets']['processed_train'])
    train_data.to_csv(processed_train, index=False)

    processed_test = os.path.join(
        settings.ROOT_PATH,
        settings.CONFIG['assets']['processed_test'])
    test_data.to_csv(processed_test, index=False)

    # Register task in log file
    log = os.path.join(settings.ROOT_PATH, settings.CONFIG['assets']['pipe_log'])
    
    prompt = f"Job: {__file__}\n"
    prompt += "Status: DONE\n"
    prompt += f"TimeStamp: {dt.datetime.now()}\n\n"

    with open(file=log, mode='a') as f:
        f.write(prompt)
    f.close()