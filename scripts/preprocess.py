import os

import pandas as pd
import datetime as dt

from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
from settings import Settings


def encode_data(df, feat_select):
    """
    
    """
    # Dictionary of numerical, categorical and ordinal features
    feats = {"numerical":None, "categorical":None, "ordinal":None}

    for key in feats.keys():
        ftype = feat_select.loc[feat_select['type_class'] == key]
        feats[key] = ftype['feature'].to_list()
    
    
    # Ordinal encoding
    for feat in feats['ordinal']:
        feat_order = feat_select.loc[feat_select['feature'] == feat, 'order']
        feat_order = feat_order.values[0].split(";")

        ord_enc = OrdinalEncoder(
            categories=[feat_order],
            handle_unknown='use_encoded_value',
            unknown_value=-1)
        ord_enc = ord_enc.fit_transform(df[[feat]])
        df.loc[df.index, feat] = ord_enc


    # One hot encoding
    for feat in feats['categorical']:
        cats = feat_select.loc[feat_select['feature'] == feat, 'order']
        cats = cats.values[0].split(";")

        ohe = OneHotEncoder(
            categories=[cats],
            drop='if_binary',
            sparse_output=False,
            handle_unknown='ignore')
        
        ohe = pd.DataFrame(
            ohe.fit_transform(df[[feat]]),
            columns=ohe.get_feature_names_out())

        df = df.join(ohe)
        df.drop(columns=feat, inplace=True)

    return df


# Initialize project settings
settings = Settings()

# Load feature selector data
feature_selector = settings.feature_selector


# Load desired features from TRAIN data to __file__
train_data = settings.invoque_data(env_var='train_set')
train_data = train_data[feature_selector['feature'].to_list()]

# Train set encoding
train_data = encode_data(df=train_data, feat_select=feature_selector)
train_data.dropna(axis=0, inplace=True)

# Save processed data in assets directory
settings.save_df(df=train_data, env_var='processed_train')


# Load desired features from TEST data to __file__
test_feats = feature_selector.loc[feature_selector['consider'] == 1]['feature'].to_list()
test_data = settings.invoque_data(env_var='test_set')
test_data = test_data[test_feats]

# Test set encoding
test_data = encode_data(df=test_data, feat_select=feature_selector)
test_data.dropna(axis=0, inplace=True)

# Save processed data in assets directory
settings.save_df(df=test_data, env_var='processed_test')


if __name__ == '__main__':

    # Register task in log file
    log = os.path.join(settings.ROOT_PATH, settings.CONFIG['assets']['pipe_log'])
    
    prompt = f"Job: {__file__}\n"
    prompt += "Status: DONE\n"
    prompt += f"TimeStamp: {dt.datetime.now()}\n\n"

    with open(file=log, mode='a') as f:
        f.write(prompt)
    f.close()