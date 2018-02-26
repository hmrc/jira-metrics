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


#Retrieves the list of teams and their corresponding ID's from an organisation
# for team in org.get_teams():
    # print team.name
    # print team.id
commit = "a1e6a64"

# for repo in team.get_repos():
#     if repo.name == "address-reputation-ingester":
#         print "Additions: " + str(repo.get_commit(commit).stats.additions)
#         print "Deletions: " + str(repo.get_commit(commit).stats.deletions)
#         print "Total Changes: " + str(repo.get_commit(commit).stats.total)
#         actual_code_changed = repo.get_commit(commit).stats.total


# for repo in user.get_repos():
#     print repo.name

# for commit in org.get_repo("taxcalc-frontend").get_commits(author="danewatts"):
#     print commit.stats.additions

for gist in user.get_gists():
    for comment in gist.get_comments():
        print comment