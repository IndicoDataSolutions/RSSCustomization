from multiprocessing.pool import ThreadPool

from flask import Flask, render_template
import feedparser
from indicoio import text_tags

app = Flask(__name__)
app.debug = True

DEFAULT = "http://www.reddit.com/.rss"

def thresholded(text_tags, minimum=0.1):
	return [category for category, prob in text_tags.items()
	        if prob > minimum]

def parsed(entry):
	return {
		'title': entry['title'],
		'link': entry['link'],
		'tags': thresholded(text_tags(entry['title']))
	}

@app.route('/')
def main():
	pool = ThreadPool(16)
	entries = pool.map(parsed, feedparser.parse(DEFAULT)['entries'])
	return render_template('main.html', entries=entries)

if __name__ == '__main__':
    app.run()