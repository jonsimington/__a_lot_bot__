import praw
from secret_settings import username, password
import time
import Queue

# main bot driver
def main():
    # initialize reddit object
    r = praw.Reddit(user_agent='UNIQUE USER AGENT')

    # authenticate to reddit
    r.login(username, password)

    print "authenticated to reddit"

    subreddit = r.get_subreddit('all')

    subreddit_comments = praw.helpers.comment_stream(r, subreddit, limit=None)

    # queue to store comments which are not able to be replied to due to the
    #   rate limit
    q = Queue.Queue(maxsize=25)

    # set containing already checked comments
    complete = set()

    for comment in subreddit_comments:
        # try to address queued comments
        if not q.empty():
            if timediff() >= 10:
                # reply to comment at front of the queue
                q_comment = q.get()
                q_comment.reply("It's 'a lot' not 'alot,' ya dingus!")
                time_last_commented = time.time()
                complete.add(q_comment.id)

        # individual words in a comment
        words = comment.body.split()
        for word in words:
            if word == "alot" and comment.id not in complete:
                # comment snarky response
                try:
                    comment.reply("It's 'a lot' not 'alot,' ya dingus!")
                    print "replied to comment {} at {}".format(comment.id, time.time())
                    time_last_commented = time.time()
                    complete.add(comment.id)
                except praw.errors.RateLimitExceeded:
                    # posting too often in a subreddit
                    # queue comment to be processed later
                    q.put(comment)
                    print "queued comment {} at {}".format(comment.id, time.time())
                    print "\tqueue size is now {}".format(q.qsize())
            else:
                continue

# calculates time in minutes between last comment and current time
def timediff():
    if time_last_commented != 0:
        return (time.time() - time_last_commented) / 60
    else:
        return -1

if __name__ == "__main__":
    time_last_commented = 0
    main()
