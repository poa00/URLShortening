from flask import Flask, request, jsonify
import shortuuid
import json
from urllib.parse import urlparse


shorturl = Flask(__name__)

# Creating a dictionary to keep track of the data
URL_LIST = {}


def get_tld(url):
    """Get top level domain/information from url

    Args:
        url (string): url to parse

    Returns:
        string : top level information of an url ... eg: https://www.yahoo.com
    """
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    hostname = parsed_url.hostname
    tld = scheme+"://"+hostname
    return tld


@shorturl.route("/")
def root():
    return "<p>this is root</p>"


@shorturl.route("/encode", methods=["POST", "GET"])
def encode():
    """generate a shortened url

    Returns:
        json: a serializable json object with a shortkey
    """
    try:
        data = request.data
        if type(data) is not str and data is not None:
            original_url = json.loads(data)
            id = shortuuid.ShortUUID().random(length=6)
            url = original_url['url']
            domain = get_tld(url)
            short_url = domain +"/" + id
            URL_LIST[id] = url

        return jsonify({"id":id,"short_url": short_url, "original_url":url})

    except Exception as e:
        return jsonify(e)


@shorturl.route("/decode", methods=["POST"])
def decode():
    """Decode a shorturl id into the original url passed before it was shortened

    Returns:
        json : the original url submitted, before the url shortening
    """
    try:
        if request.form['shorturl_id']:
            id = request.form['shorturl_id']

        return jsonify({URL_LIST[id]})

    except Exception as e:
        return json.dumps(e)

    # Needed for VSCode debugger
if __name__ == '__main__':
    shorturl.run(use_debugger=False, use_reloader=False, passthrough_errors=True)
