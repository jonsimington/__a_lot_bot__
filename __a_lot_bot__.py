import praw
from secret_settings import username, password
import time

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
    words = comment.body.split()
    for word in words:
        if word == "alot" and comment.id not in complete:
            print "found alot at comment {} at {}".format(comment.id, time.strftime("%H:%M:%S"))
            complete.add(comment.id)
            # comment snarky response here!
            comment.reply("It's 'a lot' not 'alot,' ya dingus!")
            print "replied to comment {}".format(comment.id)
        else:
            continue
