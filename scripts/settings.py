import os
import yaml


class Settings:
    def __init__(self):
        self.SCRIPTS_PATH = os.path.dirname(os.path.abspath(__file__))
        self.ROOT_PATH = os.path.dirname(self.SCRIPTS_PATH)

        with open(os.path.join(self.ROOT_PATH, "config.yaml"), 'r') as f:
            self.CONFIG = yaml.safe_load(f)
        f.close()

    def __str__(self) -> str:
        prompt = f"SCRIPTS_PATH:\t{self.SCRIPTS_PATH}\n"
        prompt += f"ROOT_PATH:\t{self.ROOT_PATH}"
        return prompt

if __name__ == '__main__':
    settings = Settings()
    print(settings.__str__())