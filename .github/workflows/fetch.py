import requests
import io
import re

GITHUB_BASE_URL = "https://github.com/"
GITHUB_EVENTS_API_BASE_URL = "https://api.github.com/users/not-ed/events"
README_FILE_PATH = "../../README.md"
MAX_EVENTS = 10

def FormatCommitCommentEvent(event):
    # TODO: include author of commit
    repo_name = event["repo"]["name"]
    repo_url = GITHUB_BASE_URL + repo_name
    comment_url = event["payload"]["comment"]["html_url"]
    return (":speech_balloon: Commented on a [commit]({}) to [{}]({}).".format(comment_url, repo_name, repo_url))

def FormatCreateEvent(event):
    created_type = event["payload"]["ref_type"]
    repo_name = event["repo"]["name"]
    repo_url = GITHUB_BASE_URL + repo_name
    if created_type == "repository":    
        return (":pencil2: Created repository [{}]({}).".format(repo_name,repo_url))
    elif created_type == "branch":
        branch_name = event["payload"]["ref"]
        branch_url = GITHUB_BASE_URL + repo_name + "/tree/" + branch_name
        return (":herb: Created [{}]({}) branch on [{}]({}).".format(branch_name, branch_url, repo_name ,repo_url))
    elif created_type == "tag":
        tag_name = event["payload"]["ref"]
        tag_url = GITHUB_BASE_URL + repo_name + "/releases/tag/" + tag_name
        return (":bookmark: Created [{}]({}) tag on [{}]({}).".format(tag_name, tag_url, repo_name ,repo_url))
    else:
        FormatUnknownEvent(event)

def FormatDeleteEvent(event):
    repo_name = event["repo"]["name"]
    repo_url = GITHUB_BASE_URL + repo_name
    deleted_type = event["payload"]["ref_type"]
    deleted_name = event["payload"]["ref"]
    if deleted_type == "branch":
        return (":x: Deleted `{}` branch in [{}]({}).".format(deleted_name, repo_name, repo_url))
    elif deleted_type == "tag":
        return (":x: Deleted `{}` tag in [{}]({}).".format(deleted_name, repo_name, repo_url))
    else:
        FormatUnknownEvent(event)

def FormatForkEvent(event):
    original_repo_name = event["repo"]["name"]
    original_repo_url = GITHUB_BASE_URL + original_repo_name
    forked_repo_name = event["payload"]["forkee"]["full_name"]
    forked_repo_url = GITHUB_BASE_URL + forked_repo_name
    return (":trident: Forked [{}]({}) into [{}]({}).".format(original_repo_name, original_repo_url, forked_repo_name, forked_repo_url))
    
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
    
#TODO
def FormatPublicEvent(event):
    FormatUnknownEvent(event)
    
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
        return (":incoming_envelope: \"[{}]({})\" in [{}]({}).".format(commit_message, commit_url, repo_name, repo_url))
    else:
        # TODO: commit links
        return (":incoming_envelope: Pushed {} commits to [{}]({}).".format(commits_pushed,repo_name,repo_url))
    
def FormatReleaseEvent(event):
    repo_name = event["repo"]["name"]
    repo_url = GITHUB_BASE_URL + repo_name
    release_title = event["payload"]["release"]["name"]
    release_url = event["payload"]["release"]["html_url"]
    return (":ship: Published a new release of [{}]({}) ([{}]({})).".format(repo_name, repo_url, release_title, release_url))
    
#TODO
def FormatSponsorshipEvent(event):
    FormatUnknownEvent(event)
    
#TODO
def FormatWatchEvent(event):
    repo_name = event["repo"]["name"]
    repo_url = GITHUB_BASE_URL + repo_name
    return (":star: Starred [{}]({}).".format(repo_name, repo_url))
    
#TODO
def FormatUnknownEvent(event):
    return None

def FormatEvent(event):
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

get_events_response = requests.get(GITHUB_EVENTS_API_BASE_URL)

read_events = []
if get_events_response.ok:
    for event in get_events_response.json():
        event_text = FormatEvent(event)
        if event_text != None:
            read_events.append(event_text + "\n\n")
            if len(read_events) == MAX_EVENTS:
                break

    with io.open(README_FILE_PATH,"r") as readme:
        contents = readme.read()
        contents = re.sub("(<!-- HISTORY_START -->)((\n|.)*)(<!-- HISTORY_END -->)", "<!-- HISTORY_START -->\n\n{}<!-- HISTORY_END -->".format("".join(read_events)),contents)

    with io.open(README_FILE_PATH, "w") as readme:
        readme.write(contents)