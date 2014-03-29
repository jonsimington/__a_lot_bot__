import praw
from secret_settings import username, password

# initialize reddit object
r = praw.Reddit(user_agent='UNIQUE USER AGENT')

# authenticate to reddit
r.login(username, password)

print "authenticated to reddit"

subreddit = r.get_subreddit('all')

subreddit_comments = praw.helpers.comment_stream(r, subreddit, limit=None)

# set containing already checked comments
complete = set()

for comment in subreddit_comments:
    # check comment for "alot"
    if comment.body == "alot" and comment.id not in complete:
        print "found alot at comment {}".format(comment.id)
        complete.add(comment.id)
        # comment snarky response here!
    else:
        continue
