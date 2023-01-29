import os, yaml

from pandas import read_csv
from seaborn import heatmap, countplot, histplot, violinplot, scatterplot
from matplotlib.pyplot import subplots, grid


# Enviroment settings and paths
CURRENT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(CURRENT)
#sys.path.append(PARENT)

with open(os.path.join(ROOT, 'config.yaml'), 'r') as f:
    config = yaml.safe_load(f)
f.close()

# Load data to __file__
train_data = read_csv(os.path.join(ROOT, config['eda']['train_set']))
test_data = read_csv(os.path.join(ROOT, config['eda']['test_set']))


# ---- NAN visualization ----
fig, ax = subplots(figsize=eval(config['eda']['img_size_large']))

# Plot specs
heatmap(data=train_data.isnull(), yticklabels=False, ax=ax)

fig.savefig(os.path.join(ROOT, 'images/nan.jpg'))


# ---- Sale price vs house style ----
fig, ax = subplots(figsize=eval(config['eda']['img_size_small']))

# Plot specs
countplot(x=train_data['SaleCondition'])
histplot(x=train_data['SaleType'], kde=True, ax=ax)
violinplot(x=train_data['HouseStyle'], y=train_data['SalePrice'], ax=ax)
scatterplot(x=train_data["Foundation"], y=train_data["SalePrice"], ax=ax)

# Annotations and styling
ax.set_title('House style effect on sale price')
grid()

fig.savefig(os.path.join(ROOT, 'images/price_house_style.jpg'))


if __name__ == '__main__':
    print("Job done")