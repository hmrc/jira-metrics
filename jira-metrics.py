#!/usr/bin/env python

from __future__ import division

import json
import sys
import ConfigParser
import os

from jira import JIRA

import datetime

config = ConfigParser.ConfigParser()
config.read("jira-metrics.ini")

jira = JIRA(server='https://jira.tools.tax.service.gov.uk/', basic_auth=(config.get("credentials", "username"), config.get("credentials", "password")))

statuses = {
    'Queue': 1,
    'Waiting to be Triaged': 1,
    'Open': 1,
    'To Do': 1,
    'Reopened': 1,
    'Dev Ready': 2,
    'Ready for Dev': 2,
    'Ready to Review TxM Assessment': 2,
    'In Dev': 3,
    'Fix in Progress': 3,
    'TxM Assessment In Progress': 3,
    'In Progress': 3,
    'In Review': 4,
    'In QA': 5,
    'Awaiting Release': 6,
    'Closed': 7,
    'Resolved': 7,
    'Done': 7
}
#Prompts user to choose what they want to do.
# print "Please select what you want to do:"
# print "1. Search specific ticket"
# print "2. View all tickets from this month"
# print "3. View tickets after a specific date"
#
# choice_selection = ''

# while choice_selection != '1' and choice_selection != '2' and choice_selection != '3':
#     choice_selection = raw_input('Enter 1, 2 or 3: ')

# if choice_selection == '1':
#     ticket_number = raw_input('Enter ticket number: ')
#     issues = [ jira.issue('TXMNT-' + str(ticket_number), expand='changelog,renderedFields') ] #Search for a specific ticket number
# elif choice_selection == '2':
#     issues = jira.search_issues('project = TXMNT AND createdDate > startOfMonth()', maxResults=1000, expand='changelog,renderedFields' ) #Search all txmnt tickets created this month
# elif choice_selection == '3':
#     date_choice = raw_input('Please enter a date: ')
#     date_choice = str(datetime.datetime.strptime(date_choice, '%d/%m/%Y').strftime('%Y/%m/%d'))
#     issues = jira.search_issues('project = TXMNT AND createdDate > "' + date_choice + '"', maxResults=1000, expand='changelog,renderedFields') #Search all txmnt tickets after a specific date

issues = jira.search_issues('project = TXMNT AND createdDate > "2016/11/01"', maxResults=1000, expand='changelog,renderedFields' )

# print "---------------------------------------------------------------------------------------------"

no_labels = ''
ticket_count = 0
recidivism_count = 0
cycle_rating_count = 0

for issue in issues:
    # print json.dumps(issue.raw, indent = 4) #Uncomment to print JSON
    cycle_threshold = 0

    for label in issue.fields.labels:
        lowerLabel = label.lower()
        if lowerLabel == 'small':
            cycle_threshold = 3
        elif lowerLabel == 'medium':
            cycle_threshold = 5
        elif lowerLabel == 'large':
            cycle_threshold = 10
        else:
            cycle_threshold = 0

    if cycle_threshold == 0:
          no_labels +=  issue.key + '\n'
    else:
        upper_bound = 100
        lower_bound = 0
        backwards_count = 0
        forwards_count = 0
        start_date = ""
        end_date = ""
        multiplier = 25
        recidivism_rating = 0
        for history in issue.changelog.histories:
            for item in history.items:
                if item.field == 'status':
                    # print item.fromString, item.to, item.toString, item.field, item.fieldtype
                    # print 'Author: ' + history.author.displayName + ' Date: ' + history.created + ' From: ' + item.fromString + ' To: '+ item.to +' ' + '' +item.toString + ''
                    if statuses[item.toString] < statuses[item.fromString]:
                        backwards_count += 1
                    if statuses[item.toString] > statuses[item.fromString]:
                        forwards_count += 1
                    if statuses[item.toString] == 1:
                        end_date = datetime.date.today()
                    if statuses[item.fromString] == 2:
                        if start_date == "":
                            start_date = history.created
                        end_date = datetime.date.today()
                    if statuses[item.toString] == 7:
                        end_date = history.created

        if (backwards_count + forwards_count) != 0:
            recidivism_rating = upper_bound * (1 - (2 * (backwards_count / (backwards_count + forwards_count))))

        if (backwards_count + forwards_count) == 0.0:
            recidivism_rating = 5

        if start_date == "": #Error handling for item going straight from queue to resolved
            start_date = end_date

        if start_date == "" and end_date == "":
            start_date = datetime.date.today()
            end_date = datetime.date.today()

        if start_date != datetime.date.today():
            start_date = datetime.datetime.strptime(start_date[:-5], "%Y-%m-%dT%H:%M:%S.%f").date()

        if end_date != datetime.date.today(): # This is needed as date format is different
            end_date = datetime.datetime.strptime(end_date[:-5], "%Y-%m-%dT%H:%M:%S.%f").date()

        #calculates the actual cycle time excluding weekends.
        all_days = [start_date + datetime.timedelta(days=x) for x in range((end_date - start_date).days + 1)]
        actual_cycle_time = sum(1 for d in all_days if d.weekday() < 5)

        if actual_cycle_time == 0: #stops division by 0 error
            actual_cycle_time = 1

        cycle_time_rating =  upper_bound - (multiplier * int(actual_cycle_time / (cycle_threshold + 1)))

        if cycle_time_rating < lower_bound:
            cycle_time_rating = lower_bound

        ticket_count += 1
        cycle_rating_count += cycle_time_rating
        recidivism_count += recidivism_rating


        # if backwards_count > 0:
            # print "backwards_count: {0} forwards_count: {1}".format(backwards_count, forwards_count)
#UNCOMMENT ALL BELOW TO SEE DETAILS

#         print "Issue: {0} reporter: {1} Rec rating: {2}".format(issue, issue.fields.reporter.displayName, recidivism_rating)
#         print "Start Date: " + str(start_date)
#         print "End Date: " + str(end_date)
#         print "Actual Cycle Time: " + str(actual_cycle_time)
#         print "Cycle Time Rating: " + str(cycle_time_rating)
#         print "------------------------------------------------------------------------------------------"
#         print ''
# print '-------------------------------------------------------'


# print "Tickets without labels:"
# print no_labels #Prints list of tickets without labels
#
# print "---------------------------"
# print "Total Number of tickets with labels: " + str(ticket_count)
# print "Average Cycle Rating: " + str(cycle_rating_count/ticket_count)
# print "Average Recidivism Rating: " + str(recidivism_count/ticket_count)
#
# if ticket_count == 0:
#     ticket_count = 1
#

average_cycle_rating = cycle_rating_count/ticket_count
average_recidivism_rating = recidivism_count/ticket_count

#Checks to see if the file metrics exists
if os.path.exists('metrics'):
    m = open('dashboard_metrics', 'w')#Write results to this file for dashbaord to read.
    f = open('metrics', 'r+') #If exists, read the file
    lines = f.readlines() #Read all the lines in the file and create a new list from them.
    last_line = lines[-1] #Assign the last line to variable
    f.close() #Close the file.
    old_cycle,old_recidivism = last_line.split(" ") #Split the values from the last line by space and assign to variables
    if("{0:.2f}".format(float(old_recidivism)) != "{0:.2f}".format(float(average_recidivism_rating))):
        #If there is no new values because there have been no updates we won't update the values in the file.
        #If there are new values then continue
        d = open('metrics', 'w') #Open the metrics file again with write permission.
        d.write(str(last_line) +"\n" + str(average_cycle_rating) + " " + str(average_recidivism_rating))#Writes over existing data as a pose to adding to the end. This speeds up file reading time.
        d.close()#Close the file

        def percent(num1, num2): #This method is used to calculate percentage change. Returns a float falue rounded to 2d.p
            num1 = float(num1)
            num2 = float(num2)
            val_diff = (num2 - num1)
            percentage = "{0:.2f}".format(((((val_diff)/num1) * 100)))
            return percentage

        cycle_percent = float(percent(old_cycle, average_cycle_rating))#Percentage change for cycle rating
        rec_percent = float(percent(old_recidivism, average_recidivism_rating))#Percentage change for recidivism rating
        print cycle_percent
        print rec_percent
        m.write(str(cycle_percent) + "," + str(rec_percent))
        m.close()
    else:
        print "No change" #If there are no changes in data return string informing.
        m.write("No change")
        m.close()
