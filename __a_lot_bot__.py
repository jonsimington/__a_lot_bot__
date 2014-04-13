import praw
from secret_settings import username, password
import datetime
import urllib2
import requests
from termcolor import colored
###############################################################################
#
#    __a_lot_bot__: a grammar nazi's best frand
#
###############################################################################

# main bot driver
def main():
    for comment in subreddit_comments:
        # individual words in a comment
        words = comment.body.split()

        # search for 'alot' in comments, comment if it's there
        reply(words, comment, complete,)

# replies to a comment
def reply(words, comment, complete):
    global NUM_COMMENTED
    for word in words:
        if word == "alot" and comment.id not in complete:
            # try to comment snarky response
            try:
                comment.reply("It's 'a lot' not '[alot](http://hyperboleandahalf.blogspot.com/2010/04/alot-is-better-than-you-at-everything.html),' ya dingus!")
                print HYPHEN_ROW
                print "|  {}  |   ".format(NUM_COMMENTED) + colored('replied','green') +  "   | {} | at | {}  | ".format(comment.id, datetime.datetime.now())
                print HYPHEN_ROW
                NUM_COMMENTED += 1

                # comment is viewed -- add comment to the complete set
                complete.add(comment.id)

            # posting too often in a subreddit
            except praw.errors.RateLimitExceeded:
                print HYPHEN_ROW
                print "|  {}  |  ".format(NUM_COMMENTED) + colored('rate limit','red') + " | {} | at | {}  | ".format(comment.id, datetime.datetime.now())
                print HYPHEN_ROW
                NUM_COMMENTED += 1
                pass

            # 403 error, perhaps the bot is banned by the subreddit it's trying
            # to comment to
            except requests.exceptions.HTTPError:
                print HYPHEN_ROW
                print "|  {}  |  ".format(NUM_COMMENTED) + colored('403 error','red') + "  | {} | at | {}  | ".format(comment.id, datetime.datetime.now())
                print HYPHEN_ROW
                NUM_COMMENTED += 1
                pass
        else:
            continue

if __name__ == "__main__":
    # counter for table labeling
    NUM_COMMENTED = 0

    # strings used to create table
    TOP_ROW = "|  #  |   status    |   id    |    |            time             |"
    HYPHEN_ROW = "|----------------------------------------------------------------|"

    # initialize reddit object
    r = praw.Reddit(user_agent='UNIQUE USER AGENT')

    # authenticate to reddit
    r.login(username, password)

    print "authenticated to reddit"

    # table formatting
    print HYPHEN_ROW
    print TOP_ROW

    subreddit = r.get_subreddit('all')

    # get list of comments from specified subreddit
    subreddit_comments = praw.helpers.comment_stream(r, subreddit, limit=None)

    # set containing already checked comments
    complete = set()

    # run the driver
    main()
