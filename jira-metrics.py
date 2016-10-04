#!/usr/bin/env python

from __future__ import division

import json
import sys
import ConfigParser

from jira import JIRA

import datetime

config = ConfigParser.ConfigParser()
config.read("jira-metrics.ini")

jira = JIRA(server='https://jira.tools.tax.service.gov.uk/', basic_auth=(config.get("credentials", "username"), config.get("credentials", "password")))

statuses = {
    'Queue': 1,
    'Open': 1,
    'To Do': 1,
    'Reopened': 1,
    'Dev Ready': 2,
    'In Progress': 3,
    'In Review': 4,
    'In QA': 5,
    'Awaiting Release': 6,
    'Closed': 7,
    'Resolved': 7,
    'Done': 7
}

# issues = jira.search_issues('project=TXMNT', maxResults=1000, expand='changelog')

issues = [ jira.issue(sys.argv[1], expand='changelog') ]

for issue in issues:
    # print json.dumps(issue.raw, indent = 4)

    upper_bound = 100
    lower_bound = 0
    backwards_count = 0
    forwards_count = 0
    start_date = ""
    end_date = ""
    multiplier = 25
    cycle_threshold = 10 # represents number of days that a cycle should last e.g. 10 represents 10 days
    recidivism_rating = 0
    for history in issue.changelog.histories:
        for item in history.items:
            if item.field == 'status':
                if statuses[item.toString] < statuses[item.fromString]:
                    backwards_count += 1
                if statuses[item.toString] > statuses[item.fromString]:
                    forwards_count += 1
                if statuses[item.toString] == 1:
                    start_date = datetime.date.today()
                    end_date = datetime.date.today()
                if start_date == "" and statuses[item.toString] > 1:
                    start_date = history.created
                    end_date = datetime.date.today()
                if statuses[item.toString] == 7:
                    end_date = history.created
                print 'Author: ' + history.author.displayName + ' Date: ' + history.created + ' From(): ' + item.fromString + ' To('+ item.to +'): ' + item.toString


    if (backwards_count + forwards_count) != 0:
        recidivism_rating = upper_bound * (1 - (2 * (backwards_count / (backwards_count + forwards_count))))

    if forwards_count == 0:
        recidivism_rating == 5

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

    # if backwards_count > 0:
        # print "backwards_count: {0} forwards_count: {1}".format(backwards_count, forwards_count)
    print "Issue: {0} reporter: {1} Rec rating: {2}".format(issue, issue.fields.reporter.displayName, recidivism_rating)
    print "Start Date: " + str(start_date)
    print "End Date: " + str(end_date)
    print "Actual Cycle Time: " + str(actual_cycle_time)
    print "Cycle Time Rating: " + str(cycle_time_rating)
