import feedparser
from feedgen.feed import FeedGenerator
from jsonpath_ng.ext import parse


def parse_feed(feed_url):
    # feed_url = feed_url or mock_feed()

    result = feedparser.parse(feed_url)
    # TODO look into encoding exception into JSON
    result.pop("bozo_exception", None)
    return result


def setup_feed(feed_json):
    # TODO override class; add ability to filter feeds on generation
    feed_generator = FeedGenerator()
    feed_generator.generator("pipe-leak")

    # map from feedparser JSON keys to corresponding feedgen entry method
    feed_map = {
        "title": "title",
        "description": "description",
        "links": "link",
        "language": "language",
        "docs": "docs",
        "rights": "rights",
        # "image": "image",
        # "logo": "image",
        # TODO add Dublin Core extension
        # "author": "author",
    }

    for feedparser_key, feedgen_method_name in feed_map.items():
        input_value = feed_json["feed"].get(feedparser_key)
        if not input_value:
            continue

        feedgen_method = getattr(feed_generator, feedgen_method_name)
        feedgen_method(input_value)
    return feed_generator


def gen_feed(feed, feed_json):
    feed_generator = feed

    # map from feedparser JSON keys to corresponding feedgen entry method
    entry_map = {
        "id": "id",
        "summary": "summary",
        "description": "description",
        "title": "title",
        "links": "link",
        # "author_detail": "author",
        # "authors": "author",
        # "author": "author",
        # "category": "category",
        # "published": "published",
        # "published_parsed": "published",
    }

    for entry in feed_json["entries"]:
        feed_entry = feed_generator.add_entry(order="append")

        for feedparser_key, feedgen_method_name in entry_map.items():
            input_value = entry.get(feedparser_key)
            if not input_value:
                continue

            feedgen_method = getattr(feed_entry, feedgen_method_name)
            feedgen_method(input_value)

    rssfeed_xml = feed_generator.rss_str(pretty=True)
    # TODO auto-detect XML encoding
    rssfeed = rssfeed_xml.decode("utf-8")
    return rssfeed


def filter_feed(feed_json, filter):
    jsonpath_expression = parse(filter)
    feed_json = list(v.value for v in jsonpath_expression.find(feed_json))

    return feed_json
