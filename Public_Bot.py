import praw
import re
import requests as request

reddit = praw.Reddit('bot1') #pulls reddit bot account data from separate PRAW.ini file
username = reddit.user.me().name
print(username)


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
        #Insert your streamable user below
        r = request.get(video_url, auth=("INSERT-STREAMABLE_USERNAME", "INSERT_STREAMABLE_PASSWORD"))
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

