import os, logging

import pandas as pd

from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
from settings import Settings


def encode_data(arr, feat_select):
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
        ord_enc = ord_enc.fit_transform(arr[[feat]])
        arr.loc[arr.index, feat] = ord_enc


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
            ohe.fit_transform(arr[[feat]]),
            columns=ohe.get_feature_names_out())

        arr = arr.join(ohe)
        arr.drop(columns=feat, inplace=True)

    return arr


# Initialize project settings
settings = Settings()

# Load feature selector data
feature_selector = settings.feature_selector


# Load desired features from TRAIN data to __file__
try:
    env_var = 'train_set'
    train_data = settings.invoque_data(env_var=env_var)
    train_data = train_data[feature_selector['feature'].to_list()]

    # Train set encoding
    train_data = encode_data(arr=train_data, feat_select=feature_selector)
    train_data.dropna(axis=0, inplace=True)

    # Save processed data in assets directory
    settings.save_df(arr=train_data, env_var='processed_train')

except (FileNotFoundError, KeyError):
    # Exception prompt
    prompt = f'An exception has occurred, either:\n'
    prompt += f'\t- "{settings.CONFIG["assets"]["train_set"]}" '
    prompt += 'not found in assets dir\n'
    prompt += f'\t- ENV_VAR "{env_var}" has no matching file in assets dir\n'
    
    # Add prompt to log file
    logging.error(prompt)


# Load desired features from TEST data to __file__
try:
    env_var = 'test_set'
    test_feats = feature_selector.loc[
        (feature_selector['consider'] == 1)]['feature'].to_list()
    test_data = settings.invoque_data(env_var=env_var)
    test_data = test_data[test_feats]

    # Test set encoding
    test_data = encode_data(arr=test_data, feat_select=feature_selector)
    test_data.dropna(axis=0, inplace=True)

    # Save processed data in assets directory
    settings.save_df(arr=test_data, env_var='processed_test')

except (FileNotFoundError, KeyError):
    # Exception prompt
    prompt = f'An exception has occurred, either:\n'
    prompt += f'\t- "{settings.CONFIG["assets"]["train_set"]}" '
    prompt += 'not found in assets dir\n'
    prompt += f'\t- ENV_VAR "{env_var}" has no matching file in assets dir\n'
    
    # Add prompt to log file
    logging.error(prompt)


if __name__ == '__main__':
    
    # Register task in log file
    prompt = f"Job in {__file__}:\n"
    prompt += "\t- Status: DONE\n"

    # Add prompt to log file
    logging.info(prompt)