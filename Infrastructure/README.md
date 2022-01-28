#JIRA Metrics for Infrastructure

Before using you'll need to install python dependencies & add your Jira API Token

Edit jira-metrics.ini and add your Personal Access Token

[credentials]
token: your token  

How to create Jira API Token 
1. Login into JIRA
2. Click on your Avatar image then click Profile
3. On the left hand side of your screen you'll see Summary & Personal Access Tokens, go to Personal Access Tokens
4. On the right you'll see a big blue button Create Token, click on it. 
5. Add a token name under the Token Name text box, your token will expire in 90 days unless you change it.
6. Click Create
7. Copy the Token created, once you click close you'll be unable to retrireve it and will need to create a new one.


pip install -r requirements.txt

To use it you shoould run python jira-metrics.py -w Number of weeks to iterate through -d Date from which you want to start. After running the script you'll have an excel file Metrics.xlsx that you need to import to google sheets so you can do graphs.

Currently we are capturing:
 - Waiting in Queue: Dev Ready to In Progress
 - Cycle time: In Progress to Dev Complete or Resolved
 - Lead Time Dev Ready to Closed if the ticket wasn't set to Dev Ready we calculate it from Open
 - Moved to left on the board
 - It has been blocked (count the time it was blocked)

So let's say that you want to get the metrics of what happened the last 6 weeks, from the 6 of December of 2021

python jira-metrics.py -w 6 -d 6/12/2021
