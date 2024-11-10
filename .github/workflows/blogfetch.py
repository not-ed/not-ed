import feedparser
from datetime import date
import io
import re

README_FILE_PATH = "../../README.md"

def RetrieveFormattedArticleLinks():
    MAX_ENTRIES = 5
    parsed_entries = 0

    article_links_text = ""
    test = feedparser.parse("https://blog.not-ed.com/rss.xml")
    for e in test["entries"]:
        pub_date = e["published_parsed"]
        parsed_date = date(pub_date.tm_year, pub_date.tm_mon, pub_date.tm_mday)
        
        article_links_text = article_links_text + "- [{}]({}) - {}.\n".format(e["title"], e["links"][0]["href"], parsed_date.strftime("%d %b. %Y"))
        
        parsed_entries = parsed_entries + 1
        if parsed_entries == MAX_ENTRIES:
            break
    return article_links_text

with io.open(README_FILE_PATH,"r") as readme:
    contents = readme.read()
    contents = re.sub("(<!-- FEED_START -->)((\n|.)*)(<!-- FEED_END -->)", "<!-- FEED_START -->\n\n{}<!-- FEED_END -->".format(RetrieveFormattedArticleLinks()), contents)

with io.open(README_FILE_PATH, "w") as readme:
    readme.write(contents)