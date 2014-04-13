import praw
from secret_settings import username, password
import datetime
import urllib2
from requests.exceptions import HTTPError
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
    for word in words:
        if word == "alot" and comment.id not in complete:
            # try to comment snarky response
            try:
                comment.reply("It's 'a lot' not 'alot,' ya dingus!")
                print "replied to comment {} at {}".format(comment.id, datetime.datetime.now())

                # comment is viewed -- add comment to the complete set
                complete.add(comment.id)

            # posting too often in a subreddit
            except praw.errors.RateLimitExceeded:
                print "\tposting too often..."
                pass

            # 403 error, perhaps the bot is banned by the subreddit it's trying
            # to comment to
            except requests.exceptions.HTTPError:
                print "\tencountered 403 error"
                pass
        else:
            continue

if __name__ == "__main__":
    # initialize reddit object
    r = praw.Reddit(user_agent='UNIQUE USER AGENT')

    # authenticate to reddit
    r.login(username, password)

    print "authenticated to reddit"

    subreddit = r.get_subreddit('all')

    # get list of comments from specified subreddit
    subreddit_comments = praw.helpers.comment_stream(r, subreddit, limit=None)

    # set containing already checked comments
    complete = set()

    # run the driver
    main()
