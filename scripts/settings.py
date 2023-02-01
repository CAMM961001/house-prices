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

        self.train_data = read_csv(
            os.path.join(self.ROOT_PATH,
            self.CONFIG['assets']['train_set']))

        self.test_data = read_csv(
            os.path.join(self.ROOT_PATH,
            self.CONFIG['assets']['test_set']))

    def __str__(self) -> str:
        prompt = f"SCRIPTS_PATH:\t{self.SCRIPTS_PATH}\n"
        prompt += f"ROOT_PATH:\t{self.ROOT_PATH}"
        return prompt

if __name__ == '__main__':
    settings = Settings()
    print(settings.__str__())