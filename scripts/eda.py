import os, sys, logging
import datetime as dt

from seaborn import heatmap, countplot, histplot, violinplot, scatterplot
from matplotlib.pyplot import subplots, grid

from settings import Settings


# Initialize project settings
settings = Settings()

try:
    train_var = 'train_set'
    train_data = settings.invoque_data(env_var=train_var)

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

except (FileNotFoundError, KeyError):
    # Exception prompt
    prompt = f'An exception has occurred, either:\n'
    prompt += f'\t- "{settings.CONFIG["assets"]["train_set"]}" '
    prompt += 'not found in assets dir\n'
    prompt += f'\t- ENV_VAR "{train_var}" has no matching file in assets dir\n'
    
    # Add prompt to log file
    logging.error(prompt)

    sys.exit(1)

if __name__ == '__main__':
    
    # Register task in log file
    prompt = f"Job in {__file__}:\n"
    prompt += "\t- Status: DONE\n"
    
    # Add prompt to log file
    logging.info(prompt)