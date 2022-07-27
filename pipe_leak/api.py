from flask import Blueprint, Response, request
from pipe_leak.transform import setup_feed, gen_feed, parse_feed, filter_feed

blueprint = Blueprint("api", __name__)


@blueprint.route("/parse")
def parse():
    feed_url = request.args.get("feed")
    feed_json = parse_feed(feed_url)

    return feed_json


@blueprint.route("/generate")
def generate():
    feed_url = request.args.get("feed")
    feed_json = parse_feed(feed_url)

    feed = setup_feed(feed_json)
    xml = gen_feed(feed, feed_json)

    # TODO auto-set mimetype based on requested type
    return Response(xml, mimetype="text/xml")


@blueprint.route("/filter")
def filt():
    feed_url = request.args.get("feed")
    feed_json = parse_feed(feed_url)

    filter = request.args.get("q")
    feed_json["entries"] = filter_feed(feed_json["entries"], filter)

    feed = setup_feed(feed_json)
    xml = gen_feed(feed, feed_json)

    # TODO auto-set mimetype based on requested type
    return Response(xml, mimetype="text/xml")
