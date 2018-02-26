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


raw_input('Press enter to begin: ')
# issues = [ jira.issue('TXMNT-500', expand='changelog,renderedFields') ]
issues = jira.search_issues('project = TXMNT AND createdDate > "2017/01/01"', maxResults=1000, expand='changelog,renderedFields' )
for issue in issues:
    # print json.dumps(issue.raw, indent = 4) #Uncomment to print JSON
    cycle_threshold = 0
    if not issue.fields.labels: #If there are no labels at all for a particular issue
        print issue.key + ' ' + issue.fields.summary
        label_to_add = raw_input('Please enter small, medium, large or epic to add this label or press ENTER to skip issue: ')
        if label_to_add == "":
            continue
        else:
            while label_to_add != ""  and (label_to_add != 'small' and label_to_add != 'medium' and label_to_add != 'large' and label_to_add != 'epic'):
                print issue.key + ' ' + issue.fields.summary
                label_to_add = raw_input('Please enter small, medium, large or epic to add this label or press ENTER to skip issue: ')
        if label_to_add == "":
            continue

        issue.fields.labels.append(label_to_add.lower())
        issue.update(fields={"labels": issue.fields.labels})

    for label in issue.fields.labels: #If there are other labels already on the issue
        lowerLabel = label.lower()
        if lowerLabel != 'small' and lowerLabel != 'medium' and lowerLabel != 'large' and lowerLabel != 'epic':
            print issue.key + ' ' + issue.fields.summary
            label_to_add = raw_input('Please enter small, medium, large or epic to add this label or press ENTER to skip issue: ')
            if label_to_add == "":
                continue
            else:
                while label_to_add != ""  and label_to_add != 'small' and label_to_add != 'medium' and label_to_add != 'large' and label_to_add != 'epic':
                    print issue.key + ' ' + issue.fields.summary
                    label_to_add = raw_input('Please enter small, medium, large or epic to add this label or press ENTER to skip issue: ')
                if label_to_add == "":
                    continue

            issue.fields.labels.append(label_to_add.lower())
            issue.update(fields={"labels": issue.fields.labels})
