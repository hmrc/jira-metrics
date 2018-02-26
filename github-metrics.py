#!/usr/bin/env python

from github import Github

import json
import sys
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("github-metrics.ini")

github = Github(config.get("credentials", "username"),config.get("credentials", "access_token"))
user = github.get_user()
org = github.get_organization("hmrc")
team = org.get_team(1921649) #Gets the details for TXM North Team

commit = "a1e6a64"

code_threshold = 50
multiplier = 5
lower_bound = 1
upper_bound = 10
actual_code_changed = 0

#Retrieves the list of teams and their corresponding ID's from an organisation
# for team in org.get_teams():
    # print team.name
    # print team.id


for repo in team.get_repos():
    if repo.name == "address-reputation-ingester":
        print "Additions: " + str(repo.get_commit(commit).stats.additions)
        print "Deletions: " + str(repo.get_commit(commit).stats.deletions)
        print "Total Changes: " + str(repo.get_commit(commit).stats.total)
        actual_code_changed = repo.get_commit(commit).stats.total

code_size_rating = upper_bound - (multiplier * int(actual_code_changed / (code_threshold + 1)))

if code_size_rating < lower_bound:
    code_size_rating = lower_bound

print "Code Size Rating: " + str(code_size_rating)
# for member in team.get_members():
#     print member.name

# for repo in user.get_repos():
#     print repo.name
