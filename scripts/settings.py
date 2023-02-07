import os
import yaml
import logging

from pandas import read_csv


class Settings:
    def __init__(self):
        self.SCRIPTS_PATH = os.path.dirname(os.path.abspath(__file__))
        self.ROOT_PATH = os.path.dirname(self.SCRIPTS_PATH)

        with open(os.path.join(self.ROOT_PATH, "config.yaml"), 'r') as f:
            self.CONFIG = yaml.safe_load(f)
        f.close()

        self.LOG_PATH = os.path.join(
            self.ROOT_PATH,
            self.CONFIG['assets']['pipe_log'])

        self.FEAT_PATH = os.path.join(
            self.ROOT_PATH,
            self.CONFIG['assets']['feature_selector'])

        # Feature selector
        features_df = read_csv(self.FEAT_PATH)
        self.feature_selector = features_df.loc[features_df['consider'] != 0]

        #Logging settings
        self.logging_settings = logging.basicConfig(
            filename=self.LOG_PATH,
            level=logging.INFO,
            filemode='a',
            datefmt='%Y-%m-%d %H:%M:%S',
            format='%(levelname)s|%(asctime)s|%(name)s|\n%(message)s')

        # Target feature
        self.target = features_df.loc[
            (features_df['consider'] == 2, 'feature')].to_list()

    def __str__(self) -> str:
        prompt = f"SCRIPTS_PATH:\t{self.SCRIPTS_PATH}\n"
        prompt += f"ROOT_PATH:\t{self.ROOT_PATH}\n"
        prompt += f"LOG_PATH:\t{self.LOG_PATH}\n"
        prompt += f"FEAT_PATH:\t{self.FEAT_PATH}"
        return prompt

    def invoque_data(self, env_var):
        df = read_csv(
            os.path.join(self.ROOT_PATH,
            self.CONFIG['assets'][env_var]))

        return df

    def save_df(self, df, env_var):
        file_path = os.path.join(
            self.ROOT_PATH,
            self.CONFIG['assets'][env_var])
        df.to_csv(file_path, index=False)
        
        

if __name__ == '__main__':
    settings = Settings()
    print(settings.__str__())