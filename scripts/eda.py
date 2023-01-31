import os, yaml

from pandas import read_csv
from seaborn import heatmap, countplot, histplot, violinplot, scatterplot
from matplotlib.pyplot import subplots, grid

from settings import Settings


# Initialize project settings
settings = Settings()

# Load train data to __file__
train_data = read_csv(
    os.path.join(settings.ROOT_PATH,
    settings.CONFIG['eda']['train_set']))



# Visualizing NAN values
fig, ax = subplots(figsize=eval(settings.CONFIG['eda']['img_size_large']))

# Plot specs
heatmap(data=train_data.isnull(), yticklabels=False, ax=ax)

# Save figure to file
fig.savefig(os.path.join(settings.ROOT_PATH, 'images/nan.jpg'))



# Visualizing sale price vs house style
fig, ax = subplots(figsize=eval(settings.CONFIG['eda']['img_size_small']))

# Plot specs
countplot(x=train_data['SaleCondition'])
histplot(x=train_data['SaleType'], kde=True, ax=ax)
violinplot(x=train_data['HouseStyle'], y=train_data['SalePrice'], ax=ax)
scatterplot(x=train_data["Foundation"], y=train_data["SalePrice"], ax=ax)

# Annotations and styling
ax.set_title('House style effect on sale price')
grid()

# Save figure to file
fig.savefig(os.path.join(settings.ROOT_PATH, 'images/price_house_style.jpg'))



if __name__ == '__main__':
    print("Job done")