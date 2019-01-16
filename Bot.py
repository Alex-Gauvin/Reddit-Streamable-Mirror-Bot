import praw
import re
import requests as request
from datetime import date

reddit = praw.Reddit('bot1')

username = reddit.user.me().name
print(username)

rHockey = reddit.subreddit("hockey")

date0 = date(1967, 5, 2)

'''for i in rHockey.stream.comments():
    if re.search("Leafs Suck", i.body, re.IGNORECASE):
        x = date.today() - date0
        i.reply("It has been " + str(x.days) + " days since the Leafs last won the cup")
'''


def get_url(comment):
    urls = re.findall('(?P<url>https?://[^\s]+)', comment.body)
    print(urls)
    for url in urls:
        if "youtube" or "youtu.be" in url:
            return url


def get_stream(comment):
    stm = 'https://api.streamable.com/import?url='
    reply = 'https://streamable.com/{}'
    link = get_url(comment)
    if link is not None:
        video_url = (stm+link)
        print(video_url)
        r = request.get(video_url, auth=("agauv066@uottawa.ca", "StreamableSucks"))
        shortcode = r.json()['shortcode']
        return reply.format(shortcode)


while True:
    for i in reddit.user.me().comments.new(limit=10):
        if re.search("!mirror", i.body, re.IGNORECASE):
            x = get_stream(i.parent())
            if x is not None:
                i.edit("Mirror: " + x)
                print('edited comment')
            else:
                print("edit failed")

