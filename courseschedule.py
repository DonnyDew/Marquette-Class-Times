import pandas as pd
from collections import defaultdict
import re

# Read the Excel file
data = pd.read_excel('class_schedule.xlsx')

# Initialize the time slots and a counter for each day and hour
time_slots = defaultdict(lambda: defaultdict(int))

# Map the single letter day representation to the full day name
day_map = {
    'M': 'Monday',
    'T': 'Tuesday',
    'W': 'Wednesday',
    'R': 'Thursday',
    'F': 'Friday',
    'S': 'Saturday',
    'U': 'Sunday',
}

def convert_to_24_hour(time):
    match = re.match(r'(\d{1,2}):(\d{2})\s*(\w{2})', time)
    if match:
        hour, minute, period = int(match.group(1)), int(match.group(2)), match.group(3)
        if period == 'PM' and hour != 12:
            hour += 12
        elif period == 'AM' and hour == 12:
            hour = 0
        return hour, minute
    else:
        raise ValueError(f'Invalid time format: {time}')

# Process each row in the data
for index, row in data.iterrows():
    meeting_pattern = row['Meeting Pattern']

    # Skip the row if the meeting pattern is empty or NaN
    if pd.isna(meeting_pattern) or not meeting_pattern:
        continue

    days, time_range = meeting_pattern.split()
    start_time, end_time = time_range.split('-')

    start_hour, start_minute = convert_to_24_hour(start_time)
    end_hour, end_minute = convert_to_24_hour(end_time)

    # Increment the counter for each day and 15-min interval
    days = days.replace("Th", "R").replace("Su", "U").replace("Tu", "T")

    for day in days:
        for curr_hour in range(24):
            for curr_minute in range(0, 60, 15):
                interval_start = (curr_hour * 60) + curr_minute
                interval_end = interval_start + 15

                class_start = (start_hour * 60) + start_minute
                class_end = (end_hour * 60) + end_minute

                if (interval_start < class_end) and (interval_end > class_start) and (interval_start != class_end):
                    time_slots[day][(curr_hour, curr_minute)] += 1


def get_time_interval(hour, minute):
    next_minute = minute + 15
    next_hour = hour
    if next_minute >= 60:
        next_minute %= 60
        next_hour += 1
    return f"{hour:02d}:{minute:02d}-{next_hour:02d}:{next_minute:02d}"

# Generate the report DataFrame
report_data = []

for day, times in time_slots.items():
    for time, count in times.items():
        hour, minute = time
        time_str = get_time_interval(hour, minute)
        full_day = day_map[day]

        # Filter times to fit when Lark office is open
        if (full_day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] and 10 <= hour < 18) or \
           (full_day == 'Saturday' and 12 <= hour < 17):
            report_data.append([full_day, time_str, count])

# Create the DataFrame
columns = ['Day of Week', 'Time Interval', '# of Classes']
report_df = pd.DataFrame(report_data, columns=columns)

# Sort the DataFrame
day_order = {day: index for index, day in enumerate(day_map.values())}
report_df['Day Order'] = report_df['Day of Week'].map(day_order)
report_df['Hour'] = report_df['Time Interval'].str.extract('(\d+):').astype(int)
report_df['Minute'] = report_df['Time Interval'].str.extract(':(\d+)-').astype(int)
report_df = report_df.sort_values(by=['Day Order', 'Hour', 'Minute']).drop(columns=['Day Order', 'Hour', 'Minute'])



