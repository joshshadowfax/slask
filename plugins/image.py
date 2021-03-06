"""!image <search term> return a random result from the google image search result for <search term>"""

from urllib import quote
import re
import requests
from random import shuffle, randint, choice

def image(searchterm, unsafe=True):
    searchterm = quote(searchterm)

    # There's a chance of pandas today
    eggs = ['panda']
    if randint(0, 100) < 10:
        searchterm = '{} {}'.format(choice(eggs), searchterm)

    safe = "&safe=" if unsafe else "&safe=active"
    searchurl = "https://www.google.com/search?tbm=isch&q={0}{1}".format(searchterm, safe)

    # this is an old iphone user agent. Seems to make google return good results.
    useragent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7"

    result = requests.get(searchurl, headers={"User-agent": useragent}).text

    images = re.findall(r'imgurl.*?(http.*?)\\', result)
    shuffle(images)

    return images[0] if images else ""

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!image (.*)", text)
    if not match: return

    searchterm = match[0]
    return image(searchterm)
