from flask import Flask, render_template, request, jsonify
from urlparse import urljoin
from werkzeug.contrib.atom import AtomFeed
import os
from bs4 import BeautifulSoup
import os
import datetime
import html2text

app = Flask(__name__)
app.debug=True

def make_external(url):
    return urljoin(request.url_root, url)

def get_articles():
	file_names = os.listdir('static/newsletters/')
	file_names.remove("example.html")
	newsletter_objects = []
	for x in range(0,len(file_names)):
		file_object = open('static/newsletters/' + str(file_names[x]), "r")
		newsletter_objects.append(file_object)
	return newsletter_objects

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)
@app.route("/")
def index():
    get_articles()
    return render_template("index.html")

@app.route("/unsubscribe")
def unsub_view():
	return render_template("unsubscribe.html")

@app.route('/recent.atom')
def recent_feed():
    try:
        feed = AtomFeed('Recent Websecweekly Releases',
                        feed_url=request.url, url=request.url_root)
        articles = get_articles()
        for article in articles:
            soup = BeautifulSoup(article.read())
            rendered_text = html2text.html2text(article.read())
            time_pub = eval(repr(modification_date(os.path.dirname(os.path.realpath(__file__)) + "/" + article.name)))
            title = "Websecweekly " + time_pub.strftime("%d-%m-%Y")
            feed.add(title, unicode(rendered_text),
                     content_type='html',
                     generator=("Websecweekly", "https://websecweekly.org", None),
                     author="Websecweekly",
                     url=make_external(article.name),
                     updated=time_pub,
                     published=time_pub)
        return feed.get_response()
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run()