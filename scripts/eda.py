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

# Load data to __file__
train_data = pd.read_csv(os.path.join(ROOT, config['eda']['train_set']))
test_data = pd.read_csv(os.path.join(ROOT, config['eda']['test_set']))


# ---- NAN visualization ----
fig, ax = plt.subplots(figsize=eval(config['eda']['img_size_large']))

# Plot specs
sns.heatmap(data=train_data.isnull(), yticklabels=False, ax=ax)

fig.savefig(os.path.join(ROOT, 'images/nan.jpg'))


# ---- Sale price vs house style ----
fig, ax = plt.subplots(figsize=eval(config['eda']['img_size_small']))

# Plot specs
sns.countplot(x=train_data['SaleCondition'])
sns.histplot(x=train_data['SaleType'], kde=True, ax=ax)
sns.violinplot(x=train_data['HouseStyle'], y=train_data['SalePrice'], ax=ax)
sns.scatterplot(x=train_data["Foundation"], y=train_data["SalePrice"], ax=ax)

# Annotations and styling
ax.set_title('House style effect on sale price')
plt.grid()

fig.savefig(os.path.join(ROOT, 'images/price_house_style.jpg'))


if __name__ == '__main__':
    print("Job done")