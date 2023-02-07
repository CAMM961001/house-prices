import os
import yaml

from pandas import read_csv


class Settings:
    def __init__(self):
        self.SCRIPTS_PATH = os.path.dirname(os.path.abspath(__file__))
        self.ROOT_PATH = os.path.dirname(self.SCRIPTS_PATH)

        with open(os.path.join(self.ROOT_PATH, "config.yaml"), 'r') as f:
            self.CONFIG = yaml.safe_load(f)
        f.close()

        self.FEAT_PATH = os.path.join(
            self.ROOT_PATH,
            self.CONFIG['assets']['feature_selector'])

        # Feature selector
        features_df = read_csv(self.FEAT_PATH)
        self.feature_selector = features_df.loc[features_df['consider'] != 0]

        # Target feature
        self.target = self.feature_selector.loc[
            (self.feature_selector['consider'] == 2, 'feature')].to_list()

    def __str__(self) -> str:
        prompt = f"SCRIPTS_PATH:\t{self.SCRIPTS_PATH}\n"
        prompt += f"ROOT_PATH:\t{self.ROOT_PATH}"
        prompt += f"FEAT_PATH:\t{self.FEAT_PATH}"
        return prompt

    def invoque_data(self, env_var):
        df = read_csv(
            os.path.join(self.ROOT_PATH,
            self.CONFIG['assets'][env_var]))
        
        return df

if __name__ == '__main__':
    settings = Settings()
    print(settings.__str__())