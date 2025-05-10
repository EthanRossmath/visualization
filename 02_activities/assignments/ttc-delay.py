# importing packages
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# importing data
ttc_df = pd.read_csv("02_activities/assignments/ttc-streetcar-delay-data-2024.csv")

# processing data

# defining a function to only keep rows where a particular column 
# has the highest frequency
def top_10_rows(df, column_name):
    """
    Returns rows of a DataFrame where the specified column's values 
    are within the top 10 most frequent values in that column.

    Args:
        df (pd.DataFrame): The input DataFrame.
        column_name (str): The name of the column to check for top values.

    Returns:
        pd.DataFrame: A DataFrame containing rows with top 10 most frequent values 
                      in the specified column.
    """
    top_10_values = df[column_name].value_counts().nlargest(10).index
    return df[df[column_name].isin(top_10_values)]

# applying the function to produce a new dataframe where the rows are
# the rows of the original dataframe with the top 10 most frequent stop
# locations
most_frequent_stops_df = top_10_rows(ttc_df, 'Location')

# Adding a new column which keeps track of the type of location
# where the streetcar stopped.
most_frequent_stops_df['Stop Location Type'] = most_frequent_stops_df['Location'].apply(
    lambda x: 'Loop' if 'LOOP' in x else (
        'Station' if 'STATION' in x else (
            'Maintenance Facility' if 'YARD' in x else 'Intersection'
        )
    )
)

# Formatting the text to be in title format and replacing spaces by
# line breaks.
most_frequent_stops_df['Location'] = most_frequent_stops_df['Location'].apply(
    lambda x: x.title().replace(' ', '\n')
)

#Reordering the rows of the dataframe by the frequency of the "Location" entry
frequency = most_frequent_stops_df['Location'].value_counts()
# dictionary of the frequencies with the "Location" entry
mapping = frequency.index.to_list() 
# categorifiying the entries of the "Location" column to allow sorting
most_frequent_stops_df['Location'] = pd.Categorical(most_frequent_stops_df['Location'], categories=mapping, ordered=True)
# sorting the rows by the frequency
most_frequent_stops_df = most_frequent_stops_df.sort_values(by='Location')

# Histogram Plot of "Location"

# Setting the style to be "whitegrid"
sns.set_style('whitegrid')

# Creating a large plot area to fit all the text
fig = plt.subplots(figsize = (10, 7))

frequent_stop_hist = sns.histplot(data=most_frequent_stops_df, x="Location",
             hue="Stop Location Type", # colouring the bars by the stop location type
             alpha=1) # setting the opacity to 1

frequent_stop_hist.set_title('Top 10 Most Frequent TTC Streetcar Delay Locations in 2024',
                             fontsize=20
                             )

frequent_stop_hist.set_xlabel('Streetcar Delay Location',
                              fontsize=12,
                              labelpad=10 # shifting axis label down for readability
                              )

frequent_stop_hist.set_ylabel('Number of Delays',
                              fontsize=12,
                              labelpad=20 # shifting axis label left for readability
                              )

plt.xticks(fontsize=9) # adjusting the font size of the ticks for readability
plt.show()