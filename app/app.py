
import requests
import urllib
from flask import Flask
from flask.templating import render_template
import sys
import os


app = Flask(__name__)

def get_context_data(**kwargs):
        context = {}
        
        token = os.environ.get("AUDIOBOOKSHELF_APPLE_PODCAST_BRIDGE_TOKEN", "")
        server_url = os.environ.get("AUDIOBOOKSHELF_APPLE_PODCAST_BRIDGE_SERVER_URL", "http://127.0.0.1")
        
        
        headers = {"Authorization": f"Bearer {token}"}
        req = requests.get(f"{server_url}/api/feeds", headers=headers)
        api_data = req.json()
        
        new_feeds = []
        
        for feed in api_data['feeds']:
            url = feed['serverAddress'] + feed['feedUrl']
            url = url._replace(scheme='podcast')
            
            name = feed['meta']['title']
            new_feeds.append({"feedUrl": url.geturl(), "title": name})
        
        context['feeds'] = new_feeds
        
        return context

@app.route('/')
def root():
    return render_template("feeds.html", **get_context_data())
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
