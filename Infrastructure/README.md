#JIRA Metrics for Infrastructure

Before using you'll need to install python dependencies 

pip install -r requirements.txt

To use it you shoould run python jira-metrics.py -w Number of weeks to iterate through -d Date from which you want to start. After running the script you'll have an excel file Metrics.xlsx that you need to import to google sheets so you can do graphs.

Currently we are capturing:
 - Waiting in Queue: Dev Ready to In Progress
 - Cycle time: In Prgoress to Dev Complete or Resolved
 - Lead Time Dev Ready to Closed if the ticket wasn't set to Dev Ready we calculate it from Open
 - Moved to left on the board
 - It has been blocked (count the time it was blocked)

So let's say that you want to get the metrics of what happened the last 6 weeks, from the 6 of December of 2021

python jira-metrics.py -w 6 -d 6/12/2021
