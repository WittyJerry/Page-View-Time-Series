import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from datetime import datetime


# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')
def parse_date(x):
    return datetime.strptime(x, "%Y-%m-%d")
df = pd.read_csv('fcc-forum-pageviews.csv',
                 index_col=['date'],
                parse_dates= ['date'],
                date_parser=parse_date,)

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & 
(df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig, ax=plt.subplots (figsize= (12,6))
    plt.title ('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.plot(df.index, df['value'])

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = pd.DatetimeIndex(df_bar.index).year
    df_bar['month'] = pd.DatetimeIndex(df_bar.index).month
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Draw bar plot
    fig = df_bar.plot.bar()
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title='Months',labels=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], prop={'size': 8})
    fig=fig.figure
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    fig, ax = plt.subplots(ncols=2, figsize=(17,7))

    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    df_box['monum'] = df_box['date'].dt.month
    df_box = df_box.sort_values('monum')

    sns.boxplot(ax=ax[0], x='year', y='value', data=df_box).set(xlabel="Year", ylabel="Page Views", title="Year-wise Box Plot (Trend)")
    sns.boxplot(ax=ax[1], x='month', y='value', data=df_box ).set(xlabel="Month", ylabel="Page Views",title="Month-wise Box Plot (Seasonality)")


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
