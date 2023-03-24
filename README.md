# Class Frequency Heatmap
This Python script reads an Excel file containing class schedules and generates a heatmap displaying the frequency of classes during different time intervals throughout the week.

## Purpose
I work at a student housing company located on Marquette University's campus. A significant aspect of my role involves contacting potential leads, who predominantly consist of Marquette students. To optimize the success of these calls, I sought to determine the most suitable time periods for reaching out to students. Gaining insights into the frequency of classes during various time slots has been instrumental in accomplishing this goal.

## Dependencies
* pandas
* seaborn
* mathplotlib
* openpyxl (for reading Excel file)

## Usage
1. Make sure you have installed the required dependencies.
2. Place the class_schedule.xlsx file in the same directory as the script.
3. Run the script. It will generate a heatmap showing the number of classes during 15-minute intervals throughout the week.

## Code Overview
The code is divided into two main sections:

## Processing the class schedule data
* Read the class_schedule.xlsx file using pandas.
* Initialize a defaultdict to store the frequency of classes during each 15-minute time interval.
* Define a mapping from single letter day representation to the full day name.
* Define a function to convert time from standard format (e.g., "12:15 PM") to a 24-hour format (e.g., 12, 15).
* Iterate through each row in the data and process the meeting patterns.
* Increment the counter for each day and 15-minute interval based on the class start and end times.
* Define a function to get the time interval in a readable format (e.g., "12:15-12:30").
* Generate a report DataFrame containing the day of the week, time interval, and the number of classes during that interval.

## Creating the heatmap
* Import the report DataFrame.
* Pivot the DataFrame for heatmap format.
* Reorder the index and columns.
* Transpose the heatmap data to flip the x and y axes.
* Sort the index in descending order.
* Define a function to convert military time to standard time and update the y-axis labels.
* Create the heatmap using seaborn and display it using matplotlib.

## Output
The output is a heatmap visualization that shows the frequency of classes during 15-minute intervals throughout the week. The heatmap's x-axis represents the days of the week, and the y-axis represents the time intervals in standard time format (e.g., "12:15 PM-12:30 PM").

## Other Tools Used
* ChatGPT