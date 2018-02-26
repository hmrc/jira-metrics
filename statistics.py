#!/usr/bin/env python

from __future__ import division

import json
import sys
import ConfigParser

from jira import JIRA

config = ConfigParser.ConfigParser()
config.read("jira-metrics.ini")

jira = JIRA(server='https://jira.tools.tax.service.gov.uk/', basic_auth=(config.get("credentials", "username"), config.get("credentials", "password")))

issues = jira.search_issues('project = TXMNT', maxResults=1000 )

#Ticket Count
in_progress_count = 0
unassigned_count = 0
unassigned_tickets = ""

#Counts for each team member
richard_count = 0
richard_tickets = ""
andy_count = 0
andy_tickets = ""
franek_count = 0
franek_tickets = ""
rick_count = 0
rick_tickets = ""
nathan_count = 0
nathan_tickets = ""
tom_count = 0
tom_tickets = ""
craig_count = 0
craig_tickets = ""
chrisj_count = 0
chrisj_tickets = ""
christ_count = 0
christ_tickets = ""

for issue in issues:
    # print json.dumps(issue.raw, indent = 4) #Uncomment to print JSON

    if str(issue.fields.status) == "In Dev" or str(issue.fields.status) == "In QA":
        in_progress_count += 1
        if issue.fields.assignee:
            if issue.fields.assignee.displayName == "Richard Shepherd":
                richard_count += 1
                richard_tickets += issue.key + ","
            if issue.fields.assignee.displayName == "Andy Hicks":
                andy_count += 1
                andy_tickets += issue.key + ","
            if issue.fields.assignee.displayName == "Franek Richardson":
                franek_count += 1
                franek_tickets += issue.key + ","
            if issue.fields.assignee.displayName == "Richard Beton":
                rick_count += 1
                rick_tickets += issue.key + ","
            if issue.fields.assignee.displayName == "Nathan Maybrey":
                nathan_count += 1
                nathan_tickets += issue.key + ","
            if issue.fields.assignee.displayName == "Thomas Pascoe":
                tom_count += 1
                tom_tickets += issue.key + ","
            if issue.fields.assignee.displayName == "Craig Pointon":
                craig_count += 1
                craig_tickets += issue.key + ","
            if issue.fields.assignee.displayName == "Chris Johnson":
                chrisj_count += 1
                chrisj_tickets += issue.key + ","
            if issue.fields.assignee.displayName == "Christopher Townson":
                christ_count += 1
                christ_tickets += issue.key + ","
        else:
            unassigned_count += 1
            unassigned_tickets += issue.key+ ","

print "Tickets in progress: " + str(in_progress_count)
print "Number of Tickets Unassigned: " + str(unassigned_count) + " (" + unassigned_tickets + ")"
print
print "Users with tickets assigned"
print "Richard: " + str(richard_count) + " (" + richard_tickets + ")"
print "Andy: " + str(andy_count) + " (" + andy_tickets + ")"
print "Franek: " + str(franek_count) + " (" + franek_tickets + ")"
print "Rick: " + str(rick_count) + " (" + rick_tickets + ")"
print "Nathan: " + str(nathan_count) + " (" + nathan_tickets + ")"
print "Tom: " + str(tom_count) + " (" + tom_tickets + ")"
print "Craig: " + str(craig_count) + " (" + craig_tickets + ")"
print "Chris J: " + str(chrisj_count) + " (" + chrisj_tickets + ")"
print "Chris T: " + str(christ_count) + " (" + christ_tickets + ")"
