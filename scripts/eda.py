import os, sys, yaml
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Enviroment settings and paths
CURRENT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(CURRENT)
#sys.path.append(PARENT)

with open(os.path.join(ROOT, 'config.yaml'), 'r') as f:
    config = yaml.safe_load(f)
f.close()

# ---- Data load ----
train_data = pd.read_csv(os.path.join(ROOT, config['eda']['train_set']))
test_data = pd.read_csv(os.path.join(ROOT, config['eda']['test_set']))

#Not a number values
fig, ax = plt.subplots(figsize=(25,10))
sns.heatmap(data=train_data.isnull(), yticklabels=False, ax=ax)
fig.savefig(os.path.join(ROOT, 'images/nan.jpg'))


if __name__ == '__main__':
    print("Hola mundo")