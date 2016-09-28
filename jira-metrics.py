#!/usr/bin/env python

from __future__ import division

import json
import sys
import ConfigParser

from jira import JIRA

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
    #print json.dumps(issue.raw, indent = 4)

    upper_bound = 100
    backwards_count = 0
    forwards_count = 0
    for history in issue.changelog.histories:
        for item in history.items:
            if item.field == 'status':
                if statuses[item.toString] < statuses[item.fromString]:
                    backwards_count += 1
                if statuses[item.toString] > statuses[item.fromString]:
                    forwards_count += 1
                print 'Author: ' + history.author.displayName + ' Date:' + history.created + ' From():' + item.fromString + ' To('+ item.to +'):' + item.toString

    if (backwards_count + forwards_count) != 0:
        recidivism_rating = upper_bound * (1 - (2 * (backwards_count / (backwards_count + forwards_count))))

    if backwards_count > 0:
        # print "backwards_count: {0} forwards_count: {1}".format(backwards_count, forwards_count)
        print "Issue: {0} reporter: {1} rec rating: {2}".format(issue, issue.fields.reporter.displayName, recidivism_rating)
