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


#Prompts user to choose what they want to do.
username = raw_input('Please enter a name:')

issues = jira.search_issues('project = "P800 Tax Calculation" AND assignee="' + username +'" AND updatedDate > -1d ORDER BY updatedDate asc' , maxResults=5 )

#Returns comments for a particular ticket
# for comment in jira.comments("PTC-1844"):
#     print(comment.body)

for issue in issues:
    # print json.dumps(issue.raw, indent = 4) #Uncomment to print JSON

    if(issue.fields.resolution is not None):
        ticketStatus = issue.fields.resolution.name
    else: ticketStatus = 'Status Not Defined'


    print ("\nIssue Number: " + issue.key + "\n" +
           "Assignee: " + issue.fields.assignee.displayName + "\n" +
           "Summary: " + issue.fields.summary + "\n" +
           "Status: " + ticketStatus + "\n")
