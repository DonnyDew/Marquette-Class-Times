from courseschedule import report_df
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Pivot the DataFrame for heatmap format
heatmap_data = report_df.pivot(index='Day of Week', columns='Time Interval', values='# of Classes')

# Reorder the index and columns
day_order_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
heatmap_data = heatmap_data.reindex(index=day_order_list)

# Transpose the heatmap data to flip the x and y axes
heatmap_data = heatmap_data.T

# Sort the index in descending order
heatmap_data.sort_index(ascending=False, inplace=True)

# Function to convert military time to standard time
def military_to_standard(time):
    hour, minute = map(int, time.split(':'))
    period = 'AM' if hour < 12 else 'PM'
    if hour == 0:
        hour = 12
    elif hour > 12:
        hour -= 12
    return f'{hour:02d}:{minute:02d} {period}'

# Convert the y-axis labels to standard time
new_index = [f'{military_to_standard(start)}-{military_to_standard(end)}' for start, end in heatmap_data.index.str.split('-')]
heatmap_data.index = new_index

# Create the heatmap and display it
plt.figure(figsize=(6, 18))
sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt="g", linewidths=.5)
plt.title('Class Frequency Heatmap')
plt.show()



