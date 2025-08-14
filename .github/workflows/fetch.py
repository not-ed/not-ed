import requests
import io
import re
from datetime import datetime

GITHUB_BASE_URL = "https://github.com/"
GITHUB_EVENTS_API_BASE_URL = "https://api.github.com/users/not-ed/events"
README_FILE_PATH = "../../README.md"
MAX_EVENTS = 10

def ShieldsBadge(text, color):
    url_text = text.replace(" ","%20")
    badge_url = "https://img.shields.io/badge/{}-{}?style=flat-square".format(url_text, color)
    return "![{}]({}) ".format(text, badge_url)

def FormatCommitCommentEvent(event):
    # TODO: include author of commit
    repo_name = event["repo"]["name"]
    repo_url = GITHUB_BASE_URL + repo_name
    comment_url = event["payload"]["comment"]["html_url"]
    return (ShieldsBadge("COMMENT","1173E0") + "Commented on a [commit]({}) to [{}]({}).".format(comment_url, repo_name, repo_url))

def FormatCreateEvent(event):
    created_type = event["payload"]["ref_type"]
    repo_name = event["repo"]["name"]
    repo_url = GITHUB_BASE_URL + repo_name
    if created_type == "repository":    
        return (ShieldsBadge("CREATE","11E05E")+ "Created repository [{}]({}).".format(repo_name,repo_url))
    elif created_type == "branch":
        branch_name = event["payload"]["ref"]
        branch_url = GITHUB_BASE_URL + repo_name + "/tree/" + branch_name
        return (ShieldsBadge("CREATE","11E05E") + "Created [{}]({}) branch on [{}]({}).".format(branch_name, branch_url, repo_name ,repo_url))
    elif created_type == "tag":
        tag_name = event["payload"]["ref"]
        tag_url = GITHUB_BASE_URL + repo_name + "/releases/tag/" + tag_name
        return (ShieldsBadge("CREATE","11E05E") + "Created [{}]({}) tag on [{}]({}).".format(tag_name, tag_url, repo_name ,repo_url))
    else:
        FormatUnknownEvent(event)

def FormatDeleteEvent(event):
    repo_name = event["repo"]["name"]
    repo_url = GITHUB_BASE_URL + repo_name
    deleted_type = event["payload"]["ref_type"]
    deleted_name = event["payload"]["ref"]
    if deleted_type == "branch":
        return (ShieldsBadge("DELETE","E01142") + "Deleted `{}` branch in [{}]({}).".format(deleted_name, repo_name, repo_url))
    elif deleted_type == "tag":
        return (ShieldsBadge("DELETE","E01142") + "Deleted `{}` tag in [{}]({}).".format(deleted_name, repo_name, repo_url))
    else:
        FormatUnknownEvent(event)

def FormatForkEvent(event):
    original_repo_name = event["repo"]["name"]
    original_repo_url = GITHUB_BASE_URL + original_repo_name
    forked_repo_name = event["payload"]["forkee"]["full_name"]
    forked_repo_url = GITHUB_BASE_URL + forked_repo_name
    return (ShieldsBadge("FORK", "CC11E0") + "Forked [{}]({}) into [{}]({}).".format(original_repo_name, original_repo_url, forked_repo_name, forked_repo_url))
    
#TODO
def FormatGollumEvent(event):
    FormatUnknownEvent(event)
    
#TODO
def FormatIssueCommentEvent(event):
    FormatUnknownEvent(event)
    
#TODO
def FormatIssuesEvent(event):
    FormatUnknownEvent(event)
    
#TODO
def FormatMemberEvent(event):
    FormatUnknownEvent(event)
    
def FormatPublicEvent(event):
    repo_name = event["repo"]["name"]
    repo_url = GITHUB_BASE_URL + repo_name
    return (ShieldsBadge("UNVEILED", "EDEDED") + "Made [{}]({}) public.".format(repo_name, repo_url))

#TODO
def FormatPullRequestEvent(event):
    FormatUnknownEvent(event)
    
#TODO
def FormatPullRequestReviewEvent(event):
    FormatUnknownEvent(event)
    
#TODO
def FormatPullRequestReviewCommentEvent(event):
    FormatUnknownEvent(event)
    
#TODO
def FormatPullRequestReviewThreadEvent(event):
    FormatUnknownEvent(event)
    
#TODO
def FormatPushEvent(event):
    repo_name = event["repo"]["name"]
    repo_url = GITHUB_BASE_URL + repo_name
    
    commits_pushed = len(event["payload"]["commits"])
    if commits_pushed == 1:
        commit_message = str(event["payload"]["commits"][0]["message"] ).split("\n")[0]
        commit_url = GITHUB_BASE_URL + repo_name + "/commit/" +(event["payload"]["commits"][0]["sha"])
        return (ShieldsBadge("COMMIT","1173E0") + "\"[{}]({})\" in [{}]({}).".format(commit_message, commit_url, repo_name, repo_url))
    else:
        # TODO: commit links
        return (ShieldsBadge("COMMIT","1173E0") + "Pushed {} commits to [{}]({}).".format(commits_pushed,repo_name,repo_url))
    
def FormatReleaseEvent(event):
    repo_name = event["repo"]["name"]
    repo_url = GITHUB_BASE_URL + repo_name
    release_title = event["payload"]["release"]["name"]
    release_url = event["payload"]["release"]["html_url"]
    return (ShieldsBadge("RELEASE", "11E05E") + "Published a new release of [{}]({}) ([{}]({})).".format(repo_name, repo_url, release_title, release_url))
    
#TODO
def FormatSponsorshipEvent(event):
    FormatUnknownEvent(event)
    
def FormatWatchEvent(event):
    repo_name = event["repo"]["name"]
    repo_url = GITHUB_BASE_URL + repo_name
    return (ShieldsBadge("STAR", "F1CE12") + "Starred [{}]({}).".format(repo_name, repo_url))
    
def FormatUnknownEvent(event):
    event_type = event["type"]
    return (ShieldsBadge("MISSINGNO","1C1C1C") + "Unknown event ({}).".format(event_type))

def FormatEventTime(event):
    event_time = datetime.strptime(event["created_at"],"%Y-%m-%dT%H:%M:%SZ")
    return event_time.strftime("%a. %d %B")

def FormatEvent(event):
    # Skip GitHub pages commits coming from Actions.
    if event["repo"]["name"] == "not-ed/not-ed.github.io":
        return None

    event_type = event["type"]
    if event_type == "CommitCommentEvent":
        return FormatCommitCommentEvent(event)
    elif event_type == "CreateEvent":
        return FormatCreateEvent(event)
    elif event_type == "DeleteEvent":
        return FormatDeleteEvent(event)
    elif event_type == "ForkEvent":
        return FormatForkEvent(event)
    elif event_type == "GollumEvent":
        return FormatGollumEvent(event)
    elif event_type == "IssueCommentEvent":
        return FormatIssueCommentEvent(event)
    elif event_type == "IssuesEvent":
        return FormatIssuesEvent(event)
    elif event_type == "MemberEvent":
        return FormatMemberEvent(event)
    elif event_type == "PublicEvent":
        return FormatPublicEvent(event)
    elif event_type == "PullRequestEvent":
        return FormatPullRequestEvent(event)
    elif event_type == "PullRequestReviewEvent":
        return FormatPullRequestReviewEvent(event)
    elif event_type == "PullRequestReviewCommentEvent":
        return FormatPullRequestReviewCommentEvent(event)
    elif event_type == "PullRequestReviewThreadEvent":
        return FormatPullRequestReviewThreadEvent(event)
    elif event_type == "PushEvent":
        return FormatPushEvent(event)
    elif event_type == "ReleaseEvent":
        return FormatReleaseEvent(event)
    elif event_type == "SponsorshipEvent":
        return FormatSponsorshipEvent(event)
    elif event_type == "WatchEvent":
        return FormatWatchEvent(event)
    else:
        return FormatUnknownEvent(event)

read_events = {}
read_event_count = 0

get_events_response = requests.get(GITHUB_EVENTS_API_BASE_URL)
if get_events_response.ok:
    for event in get_events_response.json():
        event_text = FormatEvent(event)
        if event_text != None:
            event_date = FormatEventTime(event)
            if event_date not in read_events.keys():
                if read_event_count >= MAX_EVENTS:
                    break
                read_events[event_date] = []
            read_events[event_date].append(event_text)
            read_event_count = read_event_count + 1

new_events_list = ""
for date in read_events.keys():
    new_events_list = new_events_list + "> ### {}\n".format(date)
    for event in read_events[date]:
        new_events_list = new_events_list +">\n> {}\n".format(event)
    new_events_list = new_events_list + "\n"

with io.open(README_FILE_PATH,"r") as readme:
    contents = readme.read()
    contents = re.sub("(<!-- HISTORY_START -->)((\n|.)*)(<!-- HISTORY_END -->)", "<!-- HISTORY_START -->\n\n{}<!-- HISTORY_END -->".format(new_events_list),contents)

with io.open(README_FILE_PATH, "w") as readme:
    readme.write(contents)